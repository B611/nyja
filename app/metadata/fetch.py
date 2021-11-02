from time import strptime
from typing import List
import common.networking as net
import common.export as handle_export
import common.database as database
import common.misc as misc
import bs4
import metadata.analyse
import metadata.favicon
from datetime import datetime
from indexing import blacklist
import base64


def all(args: List[str], onion_metadata={}, sema=None, session=net.session_tor()) -> List[str]:
    try:
        return misc.file_input(args)
    except:
        # Adapt to the number of indexers in arguments
        if args.URL:
            url = args.URL
            if type(args.indexers) is list:
                indexers = args.indexers
            else:
                indexers = [args.indexers]
        else:
            print('Crawling uncrawled onions from database')
            return misc.db_input(args)

    # Check for output and export arguments
    export = args.export if 'export' in args else ''
    output = args.output if 'output' in args else False

    # Fetching the data from the website
    site_meta = {}
    date = datetime.today().replace(microsecond=0)
    try:
        if database.check_if_url_blacklisted(url):
            print("URL already blacklisted")
            if sema:
                sema.release()
            return []

        # If title matches a word in blacklist, discard the entry and don't save metadata
        if blacklist.check(offline_check=url):
            print("Blacklisted offline website :", url)
            database.save_blacklisted(
                [{"site": url, "indexers": indexers}], "offline")
            if sema:
                sema.release()
            return []

        # Retrieve the metadata of the website and add the date for versioning
        # get title
        page = session.get(url, timeout=30)
        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        title = soup.find('title').__str__()[7:-8]
        site_meta['title'] = title

        # If title matches a word in blacklist, discard the entry and don't save metadata
        if blacklist.check(title=title):
            print("Blacklisted website by title :", title)
            database.save_blacklisted(
                [{"site": url, "indexers": indexers}], "title")
            if sema:
                sema.release()
            return []

        site_meta['iconData'], site_meta['iconType'] = metadata.favicon.fetch(
            session, url, soup)

        # check login
        site_meta['login'] = [
            {
                "login": metadata.analyse.check_login(soup),
                "date": date
            }
        ]
        # check captcha
        site_meta['captcha'] = [
            {
                "captcha": metadata.analyse.check_captcha(soup),
                "date": date
            }
        ]
        # get crypto
        site_meta['crypto'] = [
            {
                "crypto": metadata.analyse.check_cryptos(soup),
                "date": date
            }
        ]
        # get products
        site_meta['products'] = [
            {
                "products": metadata.analyse.check_products(soup),
                "date": date
            }
        ]

        # get html
        compressed_html = misc.compress_text(page.text)
        site_meta['html'] = [
            {
                "html": compressed_html,
                "date": date
            }
        ]
        # get mirrors
        site_meta['mirrors'] = [
            {
                "address": url,
                "indexers": indexers,
                "online": [
                    {
                    "online": True,
                    "date": date
                    }
                ]
            }
        ]
        # get online status
        site_meta['online'] = [
            {
                "online": True,
                "date": date
            }
        ]

    # If connection fails
    except Exception as e:
        # Keep track of the offline status
        database.save_offline_db(url, date)
        if sema:
            sema.release()
        if export:
            print("Data could not be retrieved, export cancelled.")
        return []

    # Actions for output and export arguments
    if not output:
        # Save the metadata in the database
        database.save_meta_db(site_meta)
        # Remove the crawled onion from uncrawled_onions
        database.del_uncrawled(url)

    if sema:
        sema.release()

    # Return global object with metadata for further use
    onion_metadata[url] = site_meta
    del onion_metadata[url]['html']
    if export:
        handle_export.json(onion_metadata[url], export)
    return onion_metadata[url]
