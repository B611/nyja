import common.misc as misc
from pymongo import MongoClient
import os

# Gobal connection to the database
client = MongoClient(
    'mongodb://%s:%s@' % (os.environ['ME_CONFIG_BASICAUTH_USERNAME'], os.environ['ME_CONFIG_BASICAUTH_PASSWORD']) +
    os.environ["MONGO_IP"])
db = client.crypto_markets

# Router to call the right stats function
def stats_router (args) :
    if args.FUNC[0] == 'history_versions_website' :
        if not args.title :
            return 'Missing arguments (title)'
        args.title = (' ').join(args.title)
        return history_versions_website(args.title)
    if args.FUNC[0] == 'history_versions_website_feature' :
        if not args.title or not args.feature :
            return 'Missing arguments (title, feature)'
        args.title = (' ').join(args.title)
        args.feature = args.feature.lower()
        return history_versions_website_feature(args.title, args.feature)
    if args.FUNC[0] == 'history_online_website' :
        if not args.title :
            return 'Missing arguments (title)'
        args.title = (' ').join(args.title)
        return history_online_website(args.title)
    if args.FUNC[0] == 'evo_website' :
        if not args.title or not args.weeks :
            return 'Missing arguments (title, weeks)'
        args.title = (' ').join(args.title)
        return evo_website(args.title, args.weeks)
    if args.FUNC[0] == 'evo_website_feature' :
        if not args.title or not args.weeks or not args.feature:
            return 'Missing arguments (title, weeks, feature)'
        args.title = (' ').join(args.title)
        args.feature = args.feature.lower()
        return evo_website_feature(args.title, args.feature, args.weeks)
    if args.FUNC[0] == 'evo_website_avg' :
        if not args.weeks :
            return 'Missing arguments (weeks)'
        return evo_website_avg(args.weeks)
    if args.FUNC[0] == 'evo_website_feature_avg' :
        if not args.feature or not args.weeks :
            return 'Missing arguments (weeks, feature)'
        args.feature = args.feature.lower()
        return evo_website_feature_avg(args.feature, args.weeks)
    if args.FUNC[0] == 'online_website' :
        if not args.title or not args.weeks :
            return 'Missing arguments (title, weeks)'
        args.title = (' ').join(args.title)
        return online_website(args.title, args.weeks)
    if args.FUNC[0] == 'online_website_avg' :
        if not args.weeks :
            return 'Missing arguments (weeks)'
        return online_website_avg(args.weeks)

# Retrieve the whole versions history of a given website
def history_versions_website (title) :
    website = db.crypto_markets.find({'title' : title})[0]

    versions_history = []
    all_versioned_fields = ['login', 'captcha', 'crypto', 'products', 'html']
    for field in all_versioned_fields :
        for i in range(len(website[field])) :
            if field == 'html' : history_entry = [website[field][i]['date'], field, misc.decompress_text(website[field][i-1][field]), misc.decompress_text(website[field][i][field])]
            else : history_entry = [website[field][i]['date'], field, website[field][i-1][field], website[field][i][field]]
            if i == 0 :
                history_entry[2] = None
                versions_history.append(history_entry)
            else :
                if history_entry not in versions_history :
                    versions_history.append(history_entry)
    versions_history.sort(key=lambda x: x[0])

    return versions_history

# Retrieve the whole versions history of a given website's feature
def history_versions_website_feature (title, feature) :
    website = db.crypto_markets.find({'title' : title})[0]

    versions_history = []
    for i in range(len(website[feature])) :
        if feature == 'html' : history_entry = [website[feature][i]['date'], feature, misc.decompress_text(website[feature][i][feature])]
        else : history_entry = [website[feature][i]['date'], feature, website[feature][i][feature]]
        if i == 0 :
            history_entry[2] = None
            versions_history.append(history_entry)
        else :
            if history_entry not in versions_history :
                versions_history.append(history_entry)
    versions_history.sort(key=lambda x: x[0])

    return versions_history


# Retrieve the whole online status history of a given website
def history_online_website (title) :
    website = db.crypto_markets.find({'title' : title})[0]

    versions_history = []
    for i in range(len(website['online'])) :
        history_entry = [website['online'][i]['date'], 'online', website['online'][i]['online']]
        if i == 0 :
            history_entry[2] = None
            versions_history.append(history_entry)
        else :
            if history_entry not in versions_history :
                versions_history.append(history_entry)
    versions_history.sort(key=lambda x: x[0])

    return versions_history

# Compute the avg nb of evolution of a given website over the number of weeks specified
def evo_website (title, weeks) :    
    website = db.crypto_markets.find({'title' : title})[0]
    
    all_versions_dates = []
    all_versioned_fields = ['login', 'captcha', 'crypto', 'products', 'html']
    for field in all_versioned_fields :
        for version in website[field] :
            if version['date'] not in all_versions_dates :
                all_versions_dates.append(version['date'])
    all_versions_dates.sort(key=lambda x: x)

    versions_dates_weeks = [[all_versions_dates[0]]]
    for date in all_versions_dates[1:] :
        if abs((date - versions_dates_weeks[-1][-1]).days/7) > int(weeks):
            versions_dates_weeks.append([date])
        else :
            versions_dates_weeks[-1].append(date)
    
    versions_weeks = 0
    for versions in versions_dates_weeks :
        versions_weeks += len(versions)
    versions_weeks = versions_weeks / len(versions_dates_weeks)

    return 'The average number of evolution / ' + str(weeks) + ' weeks of the website "' + title + '" is : ' + str(versions_weeks)

# Compute the avg nb of evolution of a given website feature over the number of weeks specified
def evo_website_feature (title, feature, weeks) :
    website = db.crypto_markets.find({'title' : title})[0]
    
    all_versions_dates = []
    for version in website[feature] :
        all_versions_dates.append(version['date'])
    all_versions_dates.sort(key=lambda x: x)

    versions_dates_weeks = [[all_versions_dates[0]]]
    for date in all_versions_dates[1:] :
        if abs((date - versions_dates_weeks[-1][-1]).days/7) > int(weeks):
            versions_dates_weeks.append([date])
        else :
            versions_dates_weeks[-1].append(date)
    
    versions_weeks = 0
    for versions in versions_dates_weeks :
        versions_weeks += len(versions)
    versions_weeks = versions_weeks / len(versions_dates_weeks)

    return 'The average number of evolution / ' + str(weeks) + ' weeks of the feature ' + str(feature) + ' of the website "' + title + '" is : ' + str(versions_weeks)

# Compute the avg nb of evolution of all websites over the number of weeks specified
def evo_website_avg (weeks) :    
    websites = db.crypto_markets.find()
    
    avg_versions_weeks = 0
    for website in websites :
        all_versions_dates = []
        all_versioned_fields = ['login', 'captcha', 'crypto', 'products', 'html']
        for field in all_versioned_fields :
            for version in website[field] :
                if version['date'] not in all_versions_dates :
                    all_versions_dates.append(version['date'])
        all_versions_dates.sort(key=lambda x: x)

        versions_dates_weeks = [[all_versions_dates[0]]]
        for date in all_versions_dates[1:] :
            if abs((date - versions_dates_weeks[-1][-1]).days/7) > int(weeks):
                versions_dates_weeks.append([date])
            else :
                versions_dates_weeks[-1].append(date)
        
        versions_weeks = 0
        for versions in versions_dates_weeks :
            versions_weeks += len(versions)
        versions_weeks = versions_weeks / len(versions_dates_weeks)
        avg_versions_weeks += versions_weeks
    avg_versions_weeks = avg_versions_weeks / websites.count()

    return 'The average number of evolution / ' + str(weeks) + ' weeks of all websites is : ' + str(avg_versions_weeks)

# Compute the avg nb of evolution of a given feature of all websites in average over the number of weeks specified
def evo_website_feature_avg (feature, weeks) :
    websites = db.crypto_markets.find()
    
    avg_versions_weeks = 0
    for website in websites :
        all_versions_dates = []
        for version in website[feature] :
            all_versions_dates.append(version['date'])
        all_versions_dates.sort(key=lambda x: x)

        versions_dates_weeks = [[all_versions_dates[0]]]
        for date in all_versions_dates[1:] :
            if abs((date - versions_dates_weeks[-1][-1]).days/7) > int(weeks):
                versions_dates_weeks.append([date])
            else :
                versions_dates_weeks[-1].append(date)

        versions_weeks = 0
        for versions in versions_dates_weeks :
            versions_weeks += len(versions)
        versions_weeks = versions_weeks / len(versions_dates_weeks)
        avg_versions_weeks += versions_weeks
    avg_versions_weeks = avg_versions_weeks / websites.count()

    return 'The average number of evolution / ' + str(weeks) + ' weeks of the feature ' + str(feature) + ' of all websites is : ' + str(avg_versions_weeks)


# Compute the avg percentage of online time of a given website over the nb of weeks specified
def online_website (title, weeks) :
    website = db.crypto_markets.find({'title' : title})[0]
    
    online_dates_weeks = [[website['online'][0]]]
    for version in website['online'][1:] :
        if abs((version['date'] - online_dates_weeks[-1][-1]['date']).days)/7 > int(weeks):
            online_dates_weeks.append([version])
        else :
            online_dates_weeks[-1].append(version)
        
    online_time_weeks = 0
    for online_dates in online_dates_weeks :
        online_time_dates = 0
        for online in online_dates :
            if online['online'] == True :
                online_time_dates += 1
        online_time_dates = online_time_dates / len(online_dates)
        online_time_weeks += online_time_dates
    online_time_weeks = online_time_weeks / len(online_dates_weeks)

    return 'The average time online / ' + str(weeks) + ' weeks of the website "' + title + '" is : ' + str(online_time_weeks)


# Compute the avg percentage of online time of all websites over the nb of weeks specified
def online_website_avg (weeks) :
    websites = db.crypto_markets.find()
    
    avg_online_time_weeks = 0
    for website in websites :
        online_dates_weeks = [[website['online'][0]]]
        for version in website['online'][1:] :
            if abs((version['date'] - online_dates_weeks[-1][-1]['date']).days)/7 > int(weeks):
                online_dates_weeks.append([version])
            else :
                online_dates_weeks[-1].append(version)

        online_time_weeks = 0
        for online_dates in online_dates_weeks :
            online_time_dates = 0
            for online in online_dates :
                if online['online'] == True :
                    online_time_dates += 1
            online_time_dates = online_time_dates / len(online_dates)
            online_time_weeks += online_time_dates
        online_time_weeks = online_time_weeks / len(online_dates_weeks)
        avg_online_time_weeks += online_time_weeks
    avg_online_time_weeks = avg_online_time_weeks / websites.count()

    return 'The average time online / ' + str(weeks) + ' weeks of all websites is : ' + str(avg_online_time_weeks)