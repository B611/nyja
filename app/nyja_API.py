#!/usr/bin/python3.8
import redis
from rq import Queue
from flask import Flask, request, jsonify, url_for
from nyja import init_parsers
import rq_dashboard
import common.database
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
redis_conn = redis.Redis(host='redis', port=6379)
queue = Queue('nyja_queue', connection=redis_conn, default_timeout=-1)
queue_misc = Queue('nyja_misc', connection=redis_conn, default_timeout=-1)
app.config.from_object(rq_dashboard.default_settings)
app.config.update(REDIS_URL='redis://redis')
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rqstatus")


def task_dispatcher(arg):
    parser = init_parsers()
    args = parser.parse_args(arg)
    return args.func(args)


def handle_nested(request):
    task = ["search"]
    query = request.get_json()['query'].split()
    for elem in query:
        task.append(elem)
    job = queue_misc.enqueue(task_dispatcher, task)
    return jsonify(query), 202, {'Access-Control-Expose-Headers': 'Location',
                              'Location': url_for('job_status', job_id=job.get_id())}


def handle_find(request):
    task = ["search"]
    query = request.get_json()['query']
    if query:
        task.append("TITLE")
        task.append(query)
    else:
        task.append('ALL')
    job = queue_misc.enqueue(task_dispatcher, task)
    return jsonify({}), 202, {'Access-Control-Expose-Headers': 'Location',
                              'Location': url_for('job_status', job_id=job.get_id())}


def handle_uncrawled():
    job = queue_misc.enqueue(common.database.get_nb_uncrawled_onions)
    return jsonify({}), 202, {'Access-Control-Expose-Headers': 'Location',
                              'Location': url_for('job_status', job_id=job.get_id())}


def handle_populate(request):
    indexer = request.get_json()['indexer']
    task = ["crawl", indexer]
    job = queue.enqueue(task_dispatcher, task)
    task = ["metadata"]
    job = queue.enqueue(f=task_dispatcher, args=[task])
    return jsonify({}), 202, {'Access-Control-Expose-Headers': 'Location',
                              'Location': url_for('job_status', job_id=job.get_id())}


def handleJSONRequests(request):
    command = request.get_json()['command']
    if command == "nested":
        return handle_nested(request)
    if command == "search":
        return handle_find(request)
    if command == "uncrawled":
        return handle_uncrawled()
    if command == "populate":
        return handle_populate(request)
    task = [command]
    save = request.get_json()['save']
    if not save:
        task.append('-o')
    if "address" in request.get_json():
        if request.get_json()['address']:
            task.append(request.get_json()['address'])
        job = queue.enqueue(task_dispatcher, task)
        return jsonify({}), 202, {'Access-Control-Expose-Headers': 'Location',
                                  'Location': url_for('job_status', job_id=job.get_id())}


@app.route('/api/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == "GET":
        config = open('/app/cron_schedule', 'r').readlines()
        return jsonify(config)
    else:
        new_config = request.get_json()['new_config']
        try:
            config = open('/app/cron_schedule', 'w')
            if new_config[-1] != '\n':
                new_config += '\n'
            config.write(new_config)
            config.close()
            return "Success"
        except:
            config = open('/app/cron_schedule', 'w')
            config.write("*/1 * * * * crontab /app/cron_schedule\n\n")
            config.close()
            return "Error"


@app.route('/api/run_task', methods=['POST'])
def run_task():
    if request.content_type.startswith('application/json'):
        return handleJSONRequests(request)
    else:
        command = request.form['command']
        save = request.form['save']
        task = [command]
        if not save:
            task.append('-o')
        file = request.files.get('file')
        file.save('/app/user_dir/' + secure_filename(file.filename))
        task.append('/app/user_dir/' + secure_filename(file.filename))
        job = queue.enqueue(task_dispatcher, task)
        return jsonify({}), 202, {'Access-Control-Expose-Headers': 'Location',
                                  'Location': url_for('job_status', job_id=job.get_id())}


@app.route('/api/status/<job_id>')
@cross_origin()
def job_status(job_id):
    job = queue.fetch_job(job_id)
    if job is None:
        job = queue_misc.fetch_job(job_id)
    if job is None:
        response = {'status': 'unknown'}
    else:
        response = {
            'status': job.get_status(),
            'result': job.result,
        }
        if job.is_failed:
            response['message'] = job.exc_info.strip().split('\n')[-1]
    return jsonify(response)


@app.route('/api', methods=['GET'])
@cross_origin()
def hello():
    return "Hello!</br></br>This is Nyja's API"
