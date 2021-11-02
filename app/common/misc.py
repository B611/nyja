import common.networking as networking
from tqdm import tqdm
from multiprocessing import Process, Manager, Semaphore
from pymongo import MongoClient
import os
import zlib
import re
import Levenshtein
from datetime import datetime


# Compare the levenshtein distance difference percentage with threshold
def compare_difference_percentage(str1, str2, percentage):
    if 100 * Levenshtein.distance(str1, str2) / float(max(len(str1), len(str2))) > percentage:
        return True
    else:
        return False


# Filter the document to match the specified date
def search_filter_date(arg, doc, spec_date):
    arg_key = arg.lower()
    # Handle if no spec_date was specified
    if spec_date != None:
        # Transform spec_date into a datetime object
        spec_date_obj = datetime.strptime(spec_date, '%d/%m/%Y')
        # Get the version of the document being first older or same than spec_date
        for i in range(len(doc[arg_key])):
            doc_date = doc[arg_key][len(
                doc[arg_key]) - i - 1]['date'].strftime('%Y-%m-%d')
            doc_date_obj = datetime.strptime(doc_date, '%Y-%m-%d')
            if doc_date_obj <= spec_date_obj:
                return doc[arg_key][len(doc[arg_key]) - i - 1]
        # If no document was stored at spec_date
        return None
    # If no date was specified perform search on the most recent version
    else:
        return doc[arg_key][-1]


# Identify the regex and set parameters
def search_regex_setup(arg_param):
    # Clean the passed regex
    regex = arg_param.split('/')
    regex = list(filter(lambda a: a != '', regex))
    # Set the regex parameter and flag if no default
    param = regex[0]
    flags = [['S', re.S], ['I', re.I], ['M', re.M], [
        'L', re.L], ['U', re.U], ['X', re.X], ['A', re.A]]
    if len(regex) > 1:
        for f in flags:
            if regex[1] == f[0]:
                flag = f[1]
    else:
        flag = re.I
    pattern = re.compile(param, flag)
    return (pattern)


# Perform OR operation between 2 lists
def search_or_operator(list1, list2):
    final_list = []
    for e in list1:
        if e not in final_list:
            final_list.append(e)
    for e in list2:
        if e not in final_list:
            final_list.append(e)
    return final_list


# Perform AND operation between 2 lists
def search_and_operator(list1, list2):
    final_list = []
    for e in list1:
        if e in list2:
            final_list.append(e)
    return final_list


# Remove the html and _id from a database document
def search_clean_doc(doc):
    # Make a copy of del to escape mutability
    doc_to_del = doc.copy()
    # Try to remove the html field if it has not been removed before
    try:
        del doc_to_del['html']
    except Exception as e:
        pass
    # Try to remove the _id field if it has not been removed before
    try:
        del doc_to_del['_id']
    except Exception as e:
        pass
    return doc_to_del


def remove_specific_key(the_dict, rubbish):
    if rubbish in the_dict:
        del the_dict[rubbish]
    for key, value in the_dict.items():
        # check for rubbish in sub dict
        if isinstance(value, dict):
            remove_specific_key(value, rubbish)

        # check for existence of rubbish in lists
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    remove_specific_key(item, rubbish)


def file_input(args_argparse):
    manager = Manager()
    onion_sites = manager.dict()
    sema = Semaphore(20)
    jobs = []
    session = networking.session_tor()

    with open(args_argparse.URL, 'r') as f:
        contents_list = f.read().splitlines()
        for content in tqdm(contents_list):
            sema.acquire()
            args_argparse.URL = content
            p = Process(target=args_argparse.func, args=(
                args_argparse, onion_sites, sema, session))
            jobs.append(p)
            p.start()
        for proc in jobs:
            proc.join()
        result = onion_sites.copy()
        remove_specific_key(result, 'html')
        return result


def db_input(args_argparse):
    manager = Manager()
    onion_sites = manager.dict()
    sema = Semaphore(64)
    jobs = []
    session = networking.session_tor()
    client = MongoClient(
        'mongodb://%s:%s@' % (os.environ['ME_CONFIG_BASICAUTH_USERNAME'], os.environ['ME_CONFIG_BASICAUTH_PASSWORD']) +
        os.environ["MONGO_IP"])
    db = client.uncrawled_onions
    try:
        uncrawled_onions = db.uncrawled_onions.find()
    except:
        print('No addresses stored in database, aborting.')
        exit()

    for url in tqdm(uncrawled_onions):
        sema.acquire()
        args_argparse.URL = url['site']
        args_argparse.indexers = url['indexers']
        p = Process(target=args_argparse.func, args=(
            args_argparse, onion_sites, sema, session))
        jobs.append(p)
        p.start()
    for proc in jobs:
        proc.join()
    result = onion_sites.copy()
    remove_specific_key(result, 'html')
    return result


def compress_text(text: str) -> bytes:
    compressor = zlib.compressobj(zlib.Z_BEST_COMPRESSION, zlib.DEFLATED, -15)
    return compressor.compress(text.encode('utf-8')) + compressor.flush()


def decompress_text(compressed_text: bytes) -> str:
    return zlib.decompress(compressed_text, wbits=-15, bufsize=zlib.DEF_BUF_SIZE).decode("utf-8")
