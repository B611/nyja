from pymongo import MongoClient
import os
import hashlib
from datetime import datetime
import common.misc as misc


# Perform advanced search in the database
def search_nested(args):
    try:
        # If user wants to retrieve all the database
        if args.NESTED[0] == 'ALL':
            print('Search for all websites :')
            print('\n')
            # Connection to the db
            client = MongoClient(
                'mongodb://%s:%s@' % (os.environ['ME_CONFIG_BASICAUTH_USERNAME'], os.environ['ME_CONFIG_BASICAUTH_PASSWORD']) +
                os.environ["MONGO_IP"])
            db = client.crypto_markets
            # Retrieve the full content of the db
            full_db_fetch = list(db.crypto_markets.find({}))
            # Return the full db
            clean_full_db = []
            for doc in full_db_fetch:
                clean_full_db.append(misc.search_clean_doc(doc))

            return clean_full_db

        # Get the arguments operators
        args_str = []
        arg_str_strings = ['TITLE', 'LOGIN', 'CAPTCHA', 'CRYPTO', 'PRODUCTS', 'HTML', 'ADDRESSES', 'INDEXERS', 'ONLINE',
                           '{', '}']
        for i in range(0, len(args.NESTED)):
            if args.NESTED[i] in arg_str_strings:
                args_str.append(args.NESTED[i])
            elif args.NESTED[i] == '||' or args.NESTED[i] == '&&':
                if args.NESTED[i - 1] in arg_str_strings or args.NESTED[i + 1] in arg_str_strings:
                    args_str.append(args.NESTED[i])

        # If a date was specified
        spec_date = None
        if args.date:
            spec_date = args.date[0]
            print('At the specified date :')
            print(args.date[0])
        # Display passed argument
        print('Search for the nested formula : ')
        print((' ').join(args.NESTED))
        print('\n')

        # Remove the { and } char for the inner computation
        args.NESTED = list(filter(lambda a: a != '{', args.NESTED))
        args.NESTED = list(filter(lambda a: a != '}', args.NESTED))

        # Get the position of arguments
        arg_content = []
        for s in arg_str_strings[:-2]:
            if s in args.NESTED:
                arg_content.append([s, args.NESTED.index(s)])
        arg_content.sort(key=lambda x: x[1])

        # Add parameters to each argument
        for i in range(len(arg_content)):
            if i + 1 < len(arg_content):
                arg_content[i][1] = args.NESTED[arg_content[i]
                                                [1] + 1:arg_content[i + 1][1] - 1]
            else:
                arg_content[i][1] = args.NESTED[arg_content[i]
                                                [1] + 1:len(args.NESTED)]

        # Group the words that are part of the same arg parameter
        operator_strings = arg_str_strings + ['||', '&&', '(', ')']
        for arg in arg_content:
            arg = arg[1]
            to_aggregate = []
            # Identify the words to aggregate
            for i in range(len(arg)):
                if arg[i] not in operator_strings:
                    if i == 0:
                        p_min_1 = operator_strings[-2]
                    else:
                        p_min_1 = arg[i - 1]
                    if i == len(arg) - 1:
                        p_plus_1 = operator_strings[-1]
                    else:
                        p_plus_1 = arg[i + 1]
                    if p_min_1 not in operator_strings or p_plus_1 not in operator_strings:
                        if len(to_aggregate) > 0:
                            if i == to_aggregate[-1][-1] + 1:
                                to_aggregate[-1].append(i)
                            else:
                                to_aggregate.append([i])
                        else:
                            to_aggregate.append([i])
            # Aggregate all words
            for param_group in to_aggregate:
                str_to_aggregate = []
                for i in param_group:
                    str_to_aggregate.append(arg[i])
                arg[param_group[0]] = (' ').join(str_to_aggregate)
            # Delete the last aggregated words
            to_delete = []
            for param_group in to_aggregate:
                to_delete.append(param_group[1:])
            del_j = 0
            for i in range(len(to_delete)):
                for j in range(len(to_delete[i])):
                    to_delete[i][j] = to_delete[i][j] - del_j
                    del_j += 1
            for delete_group in to_delete:
                for i in delete_group:
                    del arg[i]

        # Compute each arg result
        args_results = []
        for a in arg_content:
            args_results.append(
                [a[0], search_nested_arg_result(a[0], a[1], spec_date)])

        # Apply operators on args and return
        return (search_nested_arg_operators(args_str, args_results))
    except Exception as err:
        return 'Nested expression not recognised'


def search_nested_arg_operators(args_str, args_results):
    # If only one parameter is given (no brackets, no operator)
    if '{' not in args_str and '}' not in args_str:
        return (args_results[0][1])

    # Identify arg brackets and their position
    open_pos = [index for index, element in enumerate(
        args_str) if element == '{']
    close_pos = [index for index, element in enumerate(
        args_str) if element == '}']

    # Get the arg brackets content from smallest to biggest
    small_brackets = []
    big_brackets = []
    for c in close_pos:
        open_c = -1
        for o in open_pos:
            if o < c and o > open_c:
                open_c = o
        open_pos.remove(open_c)
        bracket_content = args_str[open_c + 1:c]
        if '{' in bracket_content or '}' in bracket_content:
            big_brackets.append(bracket_content)
        else:
            small_brackets.append(bracket_content)

    # Compute the small arg brackets results
    brackets_results = []
    for s in small_brackets:
        brackets_results.append([s])
        small_brackets_result_list_1 = list(
            filter(lambda a: a[0] == s[0], args_results))
        small_brackets_result_list_2 = list(
            filter(lambda a: a[0] == s[2], args_results))
        if '||' in s:
            brackets_results[-1].append(
                misc.search_or_operator(small_brackets_result_list_1[0][1], small_brackets_result_list_2[0][1]))
        elif '&&' in s:
            brackets_results[-1].append(
                misc.search_and_operator(small_brackets_result_list_1[0][1], small_brackets_result_list_2[0][1]))

    # Compute the big brackets results
    for b in big_brackets:
        # Identify the brackets and add previous results
        b_str = ' '.join(b)
        b_results = []
        brackets_results.append([b.copy()])
        for r in brackets_results[:-1]:
            r_str = ' '.join(r[0])
            if r_str in b_str:
                b_results.append(r[1])
                brackets_results.remove(r)
                for e in r[0]:
                    b.remove(e)
        # Remove brackets
        b = list(filter(lambda a: a != '{', b))
        b = list(filter(lambda a: a != '}', b))

        # Add the other result list if necessary and apply operators
        if len(b_results) == 2:
            if '||' in b:
                brackets_results[-1].append(
                    misc.search_or_operator(b_results[0], b_results[1]))
            elif '&&' in b:
                brackets_results[-1].append(
                    misc.search_and_operator(b_results[0], b_results[1]))
        else:
            if '||' in b:
                big_bracket_results_list = list(
                    filter(lambda a: a[0] == b[1 - b.index('||')], args_results))
                b_results.append(big_bracket_results_list[0][1])
                brackets_results[-1].append(
                    misc.search_or_operator(b_results[0], b_results[1]))
            elif '&&' in b:
                big_bracket_results_list = list(
                    filter(lambda a: a[0] == b[1 - b.index('&&')], args_results))
                b_results.append(big_bracket_results_list[0][1])
                brackets_results[-1].append(
                    misc.search_and_operator(b_results[0], b_results[1]))

    return brackets_results[-1][1]


def search_nested_arg_result(arg, arg_params, spec_date):
    # Connection to the db
    client = MongoClient(
        'mongodb://%s:%s@' % (os.environ['ME_CONFIG_BASICAUTH_USERNAME'], os.environ['ME_CONFIG_BASICAUTH_PASSWORD']) +
        os.environ["MONGO_IP"])
    db = client.crypto_markets

    # Retrieve the full content of the db
    # CAREFUL, MAY NOT BE SCALABLE WITH A BIG DATABASE
    full_db_fetch = list(db.crypto_markets.find({}))

    # If only one parameter is given (no brackets, no operator)
    if '(' not in arg_params and ')' not in arg_params:
        result = []
        for doc in full_db_fetch:
            if search_if_arg(arg, arg_params[0], doc, spec_date):
                result.append(misc.search_clean_doc(doc))
        return (result)

    # Identify brackets and their position
    open_pos = [index for index, element in enumerate(
        arg_params) if element == '(']
    close_pos = [index for index, element in enumerate(
        arg_params) if element == ')']

    # Get the brackets content from smallest to biggest
    small_brackets = []
    big_brackets = []
    for c in close_pos:
        open_c = -1
        for o in open_pos:
            if o < c and o > open_c:
                open_c = o
        open_pos.remove(open_c)
        bracket_content = arg_params[open_c + 1:c]
        if '(' in bracket_content or ')' in bracket_content:
            big_brackets.append(bracket_content)
        else:
            small_brackets.append(bracket_content)

    # Compute the small brackets results
    brackets_results = []
    for s in small_brackets:
        brackets_results.append([s])
        small_bracket_left_result = []
        small_bracket_right_result = []
        for doc in full_db_fetch:
            if search_if_arg(arg, s[0], doc, spec_date):
                small_bracket_left_result.append(misc.search_clean_doc(doc))
            if search_if_arg(arg, s[2], doc, spec_date):
                small_bracket_right_result.append(misc.search_clean_doc(doc))
        if '||' in s:
            brackets_results[-1].append(misc.search_or_operator(
                small_bracket_left_result, small_bracket_right_result))
        elif '&&' in s:
            brackets_results[-1].append(misc.search_and_operator(
                small_bracket_left_result, small_bracket_right_result))

    # Compute the big brackets results
    for b in big_brackets:
        # Identify the brackets and add previous results
        b_str = ' '.join(b)
        b_results = []
        brackets_results.append([b.copy()])
        for r in brackets_results[:-1]:
            r_str = ' '.join(r[0])
            if r_str in b_str:
                b_results.append(r[1])
                brackets_results.remove(r)
                for e in r[0]:
                    b.remove(e)
        # Remove brackets
        b = list(filter(lambda a: a != '(', b))
        b = list(filter(lambda a: a != ')', b))

        # Add the other result list if necessary and apply operators
        if len(b_results) == 2:
            if '||' in b:
                brackets_results[-1].append(
                    misc.search_or_operator(b_results[0], b_results[1]))
            elif '&&' in b:
                brackets_results[-1].append(
                    misc.search_and_operator(b_results[0], b_results[1]))
        else:
            b_results.append([])
            if '||' in b:
                for doc in full_db_fetch:
                    if search_if_arg(arg, b[1 - b.index('||')], doc, spec_date):
                        b_results[-1].append(misc.search_clean_doc(doc))
                brackets_results[-1].append(
                    misc.search_or_operator(b_results[0], b_results[1]))
            elif '&&' in b:
                for doc in full_db_fetch:
                    if search_if_arg(arg, b[1 - b.index('&&')], doc, spec_date):
                        b_results[-1].append(misc.search_clean_doc(doc))
                brackets_results[-1].append(
                    misc.search_and_operator(b_results[0], b_results[1]))

    return brackets_results[-1][1]


# Perform the if statement to filter documents
def search_if_arg(arg, arg_param, doc, spec_date):
    # For versionned args, filter the doc to match the specified date
    if arg != 'TITLE' and arg != 'ADDRESSES' and arg != 'INDEXERS':
        doc_at_date = misc.search_filter_date(arg, doc, spec_date)
        if not doc_at_date:
            return False

    # Get the regex setup
    pattern = misc.search_regex_setup(arg_param)

    # Perform the doc filtering
    if arg == 'TITLE':
        return bool(pattern.search(doc['title']))
    elif arg == 'LOGIN':
        return bool(pattern.search(str(doc_at_date['login'])))
    elif arg == 'CAPTCHA':
        return bool(pattern.search(str(doc_at_date['captcha'])))
    elif arg == 'CRYPTO':
        return bool(list(filter(pattern.search, doc_at_date['crypto'])))
    elif arg == 'PRODUCTS':
        product_keys = doc_at_date['products'].keys()
        for key in product_keys:
            filtered_products = list(
                filter(pattern.search, doc_at_date['products'][key]))
            if filtered_products:
                return True
        return False
    elif arg == 'HTML':
        return bool(pattern.search(misc.decompress_text(doc_at_date['html'])))
    elif arg == 'ADDRESSES':
        for mirror in doc['mirrors']:
            if pattern.search(mirror['address']) != None:
                return True
        return False
    elif arg == 'INDEXERS':
        for mirror in doc['mirrors']:
            for indexer in mirror['indexers']:
                if pattern.search(indexer) != None:
                    return True
        return False
    elif arg == 'ONLINE':
        return bool(pattern.search(str(doc_at_date['online'])))


def get_nb_uncrawled_onions():
    client = MongoClient(
        'mongodb://%s:%s@' % (os.environ['ME_CONFIG_BASICAUTH_USERNAME'], os.environ['ME_CONFIG_BASICAUTH_PASSWORD']) +
        os.environ["MONGO_IP"])
    db = client.uncrawled_onions
    return db.uncrawled_onions.count()


# Add an onion address in the list to be crawled
def save_uncrawled(uncrawled):
    print('Saving onions in database...')

    # Connection to MongoDB
    client = MongoClient(
        'mongodb://%s:%s@' % (os.environ['ME_CONFIG_BASICAUTH_USERNAME'], os.environ['ME_CONFIG_BASICAUTH_PASSWORD']) +
        os.environ["MONGO_IP"])
    db = client.uncrawled_onions

    # For each site
    for site in uncrawled:
        # print(site)
        # Find whether this address is already saved
        db_fetched = db.uncrawled_onions.find({"site": site["site"]})
        # If the site is in the db
        if db_fetched.count():
            for db_site in db_fetched:
                # Verify if indexer is new for this onion entry
                if db_site["indexers"] != site["indexers"] and (site["indexers"][0] not in db_site["indexers"]):
                    # Add the indexer to the database
                    db_site["indexers"] += site["indexers"]
                    # Update the database
                    db.uncrawled_onions.update_one(
                        {"_id": db_site["_id"]}, {"$set": db_site})
        # If the site isn't already saved
        else:
            # Insert the site in the db
            db.uncrawled_onions.insert(site)


def check_if_url_blacklisted(checked_url: str) -> bool:
    # Connection to MongoDB
    client = MongoClient(
        'mongodb://%s:%s@' % (os.environ['ME_CONFIG_BASICAUTH_USERNAME'], os.environ['ME_CONFIG_BASICAUTH_PASSWORD']) +
        os.environ["MONGO_IP"])
    db = client.blacklisted

    checked_url = hashlib.sha256(checked_url.encode("utf-8")).hexdigest()
    blacklisted_urls = db.blacklisted.find(
        {"site": checked_url}, {"site": 1, "_id": 0, "indexers": 0})

    return bool(blacklisted_urls.count())


# Add an onion address in the list to be crawled
def save_blacklisted(blacklisted_urls, motive):
    print('Saving blacklisted onions in database...')
    # Connection to MongoDB
    client = MongoClient(
        'mongodb://%s:%s@' % (os.environ['ME_CONFIG_BASICAUTH_USERNAME'], os.environ['ME_CONFIG_BASICAUTH_PASSWORD']) +
        os.environ["MONGO_IP"])
    db = client.blacklisted
    db_offline = client.offline_urls

    # For each site
    for site in blacklisted_urls:
        # Hash the URL, to not store links to illegal website
        site['site'] = hashlib.sha256(site['site'].encode('utf-8')).hexdigest()
        # Find whether this address is already saved
        db_fetched = db.blacklisted.find({"site": site["site"]})

        # If the site isn't already saved
        if not db_fetched.count():
            # Delete the offline onion
            db_offline.offline_urls.delete_one({"address": site["site"]})
            # Add the motive
            site['motive'] = motive
            # Insert the site in the db
            db.blacklisted.insert(site)


# Remove an onion address from the list to be crawled
def del_uncrawled(onion_url):
    # Connection to MongoDB
    client = MongoClient(
        'mongodb://%s:%s@' % (os.environ['ME_CONFIG_BASICAUTH_USERNAME'], os.environ['ME_CONFIG_BASICAUTH_PASSWORD']) +
        os.environ["MONGO_IP"])
    db = client.uncrawled_onions

    # Delete the uncrawled onion
    db.uncrawled_onions.delete_one({"site": onion_url})


# Check whether a URL needs to be ban as offline
def ban_offline_check(url):
    # Connection to MongoDB
    client = MongoClient(
        'mongodb://%s:%s@' % (os.environ['ME_CONFIG_BASICAUTH_USERNAME'], os.environ['ME_CONFIG_BASICAUTH_PASSWORD']) +
        os.environ["MONGO_IP"])
    # Search for the url in the db
    crypto_market = client.crypto_markets.crypto_markets.find(
        {"mirrors.address": url})
    offline_url = client.offline_urls.offline_urls.find({'address': url})
    # Generate current date for comparison
    date = datetime.today().replace(microsecond=0)
    # If url is in crypto_markets
    if crypto_market.count():
        website_checked = crypto_market[0]
    # If url is in offline_urls
    elif offline_url.count():
        website_checked = offline_url[0]
    # If url is in none of them
    else:
        return False
    # Check 5 times
    if len(website_checked['online']) >= 5:
        # Check last 5 times offline
        last_five_offline = True
        for i in range(1, 5):
            if website_checked['online'][len(website_checked['online']) - i]['online'] == True:
                last_five_offline = False
        if website_checked['online'][len(website_checked['online']) - 5]['online'] == True:
            last_five_offline = False
        else:
            first_offline_date = website_checked['online'][len(
                website_checked['online']) - 5]['date']
        if last_five_offline:
            # Check 2 weeks
            if abs((date - first_offline_date).days) > 14:
                return True
    return False


# Save the online state of websites or urls when offline
def save_offline_db(url, date):
    # Connection setup to the db
    client = MongoClient(
        'mongodb://%s:%s@' % (os.environ['ME_CONFIG_BASICAUTH_USERNAME'], os.environ['ME_CONFIG_BASICAUTH_PASSWORD']) +
        os.environ["MONGO_IP"])
    db_crypto_markets = client.crypto_markets
    # If url is in crypto_markets
    crypto_market = db_crypto_markets.crypto_markets.find({"mirrors.address": url})
    if crypto_market.count():
        crypto_market = crypto_market[0]
        # Select mirrors object corresponding to addr
        db_entry = next(
            entry for entry in crypto_market['mirrors'] if entry['address'] == url)
        # Add the last online status record in the mirror
        db_entry['online'].append(
            {
                'online': False,
                'date': date
            }
        )
        # If the last global online status of the website is not today
        if abs((crypto_market['online'][-1]['date'] - date).days) > 1 :
            # Add a global online status to offline
            crypto_market['online'].append(
                {
                    'online': False,
                    'date': date
                }
            )
        # Update the site object by adding the new online status in the mirror and the global online status
        db_crypto_markets.crypto_markets.update_one({"title": crypto_market['title']},
                                     {"$set": {"mirrors": crypto_market["mirrors"], "online": crypto_market["online"]}})
        return 0

    # If url is not in crypto markets
    db_offline_urls = client.offline_urls
    offline_url = db_offline_urls.offline_urls.find({'address': url})
    if offline_url.count():
        # Update the url online status
        offline_url = offline_url[0]
        offline_url['online'].append(
            {
                'online': False,
                'date': date
            }
        )
        # Update by adding the new url online status
        db_offline_urls.offline_urls.update_one({"address": url}, {
            "$set": {"online": offline_url['online']}})
        return 0

    # If url is not in offline_urls, insert it
    db_offline_urls.offline_urls.insert(
        {
            'address': url,
            'online': [
                {
                    'online': False,
                    'date': date
                }
            ]
        }
    )
    return 0


def del_offline_url(url):
    # Connection setup to the db
    client = MongoClient(
        'mongodb://%s:%s@' % (os.environ['ME_CONFIG_BASICAUTH_USERNAME'], os.environ['ME_CONFIG_BASICAUTH_PASSWORD']) +
        os.environ["MONGO_IP"])
    db_offline_urls = client.offline_urls
    # Delete the offline url
    db_offline_urls.offline_urls.delete_one({'address': url})
    return 0


# Save the metadata of a website
def save_meta_db(site_meta):
    # Connection setup to the db
    client = MongoClient(
        'mongodb://%s:%s@' % (os.environ['ME_CONFIG_BASICAUTH_USERNAME'], os.environ['ME_CONFIG_BASICAUTH_PASSWORD']) +
        os.environ["MONGO_IP"])
    db = client.crypto_markets
    print('Saving metadata in database...')
    # Generate new date for the update
    date = datetime.today().replace(microsecond=0)
    # Check if the site is already registered
    db_fetched = db.crypto_markets.find_one({'title': site_meta['title']})
    # If not, insert it
    if not db_fetched:
        # Modify the online object with the the online status history of this URL
        offline_url = client.offline_urls.offline_urls.find(
            {'address': site_meta['mirrors'][0]['address']})
        if offline_url.count():
            site_meta["mirrors"][0]["online"] += offline_url[0]["online"]
            site_meta["mirrors"][0]["online"].sort(key=lambda x: x["date"])
            del_offline_url(site_meta['mirrors'][0]['address'])
        db.crypto_markets.insert_one(site_meta)
    # If the site is already registered
    else:
        print('Updating metadata in database...')
        # If addr is not registered in the mirrors yet, add to mirror
        if not any(entry['address'] == site_meta['mirrors'][0]['address'] for entry in db_fetched['mirrors']):
            # Modify site_meta mirror online status with offline_urls
            offline_url = client.offline_urls.offline_urls.find({'address': site_meta['mirrors'][0]['address']})
            if offline_url.count():
                site_meta["mirrors"][0]['online'] += offline_url[0]["online"]
                site_meta["mirrors"][0]['online'].sort(key=lambda x: x["date"])
                del_offline_url(site_meta['mirrors'][0]['address'])
            # Modify the db_fetched mirror object by adding the site_meta object
            db_fetched["mirrors"].append(site_meta['mirrors'][0])
            # Update the site object by adding the mirror and its online status
            db.crypto_markets.update_one({"title": site_meta['title']}, {
                "$set": {"mirrors": db_fetched["mirrors"]}})
        # If addr already registered in the mirrors, update indexers and the online status
        else:
            # Select mirrors object corresponding to addr
            db_entry = next(
                entry for entry in db_fetched['mirrors'] if entry['address'] == site_meta['mirrors'][0]['address'])
            # Add the last online status record
            db_entry['online'].append(site_meta['mirrors'][0]['online'][0])
            # Check if each indexer is already registered
            for i in site_meta['mirrors'][0]['indexers']:
                if i not in db_entry['indexers']:
                    # Update the mirror's indexers
                    db_entry["indexers"].append(i)
            # Update the site object by adding the indexer and the mirror online status
            db.crypto_markets.update_one({"title": site_meta['title']},
                                         {"$set": {"mirrors": db_fetched["mirrors"]}})

        # Modify the global online status of the website
        if abs((db_fetched['online'][-1]['date'] - date).days) == 1 :
            db_fetched['online'][-1] = site_meta['online'][0]
        else :
            db_fetched['online'].append(site_meta['online'][0])
        # Update the site global online status
        db.crypto_markets.update_one({"title": site_meta['title']}, {
            "$set": {"online": db_fetched["online"]}})

        # Check for changes in login
        login = site_meta['login'][-1]['login']
        # If login status changed
        if db_fetched['login'][-1]['login'] != login:
            # Modify the login status list of objects
            db_fetched["login"].append(
                {
                    'login': login,
                    'date': date
                }
            )
            # Update by adding the new login status
            db.crypto_markets.update_one({"title": site_meta['title']}, {
                "$set": {"login": db_fetched["login"]}})
        # If login status hasn't change
        else:
            # Modify the date of the last login status object
            db_fetched["login"][-1]["date"] = date
            # Updating the last login status object
            db.crypto_markets.update_one({"title": site_meta['title']}, {
                "$set": {"login": db_fetched["login"]}})

        # Check for changes in captcha
        captcha = site_meta['captcha'][-1]['captcha']
        # If captcha status changed
        if db_fetched['captcha'][-1]['captcha'] != captcha:
            # Modify the captcha status list of objects
            db_fetched["captcha"].append(
                {
                    'captcha': captcha,
                    'date': date
                }
            )
            # Update by adding the new captcha status
            db.crypto_markets.update_one({"title": site_meta['title']}, {
                "$set": {"captcha": db_fetched["captcha"]}})
        # If captcha status hasn't change
        else:
            # Modify the date of the last captcha status object
            db_fetched["captcha"][-1]["date"] = date
            # Updating the last captcha status object
            db.crypto_markets.update_one({"title": site_meta['title']}, {
                "$set": {"captcha": db_fetched["captcha"]}})

        # Check for changes in crypto
        crypto = site_meta['crypto'][-1]['crypto']
        # If crypto changed
        if db_fetched['crypto'][-1]['crypto'] != crypto:
            # Modify the crypto list of objects
            db_fetched["crypto"].append(
                {
                    'crypto': crypto,
                    'date': date
                }
            )
            # Update by adding the new crypto
            db.crypto_markets.update_one({"title": site_meta['title']}, {
                "$set": {"crypto": db_fetched["crypto"]}})
        # If crypto hasn't change
        else:
            # Modify the date of the last crypto object
            db_fetched["crypto"][-1]["date"] = date
            # Updating the last crypto object
            db.crypto_markets.update_one({"title": site_meta['title']}, {
                "$set": {"crypto": db_fetched["crypto"]}})

        # Check for changes in products
        products = site_meta['products'][-1]['products']
        # If products changed
        if db_fetched['products'][-1]['products'] != products:
            # Modify the products list of objects
            db_fetched["products"].append(
                {
                    'products': products,
                    'date': date
                }
            )
            # Update by adding the new products
            db.crypto_markets.update_one({"title": site_meta['title']}, {
                "$set": {"products": db_fetched["products"]}})
        # If products hasn't change
        else:
            # Modify the date of the last products object
            db_fetched["products"][-1]["date"] = date
            # Updating the last products object
            db.crypto_markets.update_one({"title": site_meta['title']}, {
                "$set": {"products": db_fetched["products"]}})

        # Check for changes in html
        html = site_meta['html'][-1]['html']
        # If html changed
        if misc.compare_difference_percentage(misc.decompress_text(db_fetched['html'][-1]['html']),
                                              misc.decompress_text(html), 5):
            # Modify the html list of objects
            db_fetched["html"].append(
                {
                    'html': html,
                    'date': date
                }
            )
            # Update by adding the new html
            db.crypto_markets.update_one({"title": site_meta['title']}, {
                "$set": {"html": db_fetched["html"]}})
        # If html hasn't change
        else:
            # Modify the date of the last html object
            db_fetched["html"][-1]["date"] = date
            # Updating the last html object
            db.crypto_markets.update_one({"title": site_meta['title']}, {
                "$set": {"html": db_fetched["html"]}})


# Get list of past crawled indexers
def get_crawled_indexers():
    client = MongoClient(
        'mongodb://%s:%s@' % (os.environ['ME_CONFIG_BASICAUTH_USERNAME'], os.environ['ME_CONFIG_BASICAUTH_PASSWORD']) +
        os.environ["MONGO_IP"])
    # Going to the crypto markets collection in the crypto markets table
    db = client.crypto_markets.crypto_markets
    # Creation of the pipeline to process the data
    pipeline = [
        {"$unwind": "$mirrors"},
        {"$unwind": "$mirrors.indexers"},
        {"$group": {"_id": {}, "set": {"$addToSet": "$mirrors.indexers"}}},
    ]
    # Aggregate the pipeline to retreive the wanted data
    fetched_indexers = db.aggregate(pipeline)
    # Return the result
    for i in fetched_indexers:
        return i["set"]


# Get list of past crawled URLs
def get_crawled_addresses():
    client = MongoClient(
        'mongodb://%s:%s@' % (os.environ['ME_CONFIG_BASICAUTH_USERNAME'], os.environ['ME_CONFIG_BASICAUTH_PASSWORD']) +
        os.environ["MONGO_IP"])
    # Going to the crypto markets collection in the crypto markets table
    db = client.crypto_markets.crypto_markets
    # Creation of the pipeline to process the data
    pipeline = [
        {"$unwind": "$mirrors"},
        {"$group": {"_id": {}, "set": {"$addToSet": "$mirrors.address"}}},
    ]
    # Aggregate the pipeline to retreive the wanted data
    fetched_mirrors = db.aggregate(pipeline)
    # Return the result
    for m in fetched_mirrors:
        return m["set"]
