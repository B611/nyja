from typing import List
import bs4
import re
import common.networking as networking
import common.misc as misc
import common.database as database
import common.export as handle_export
from urllib.parse import urlparse
from indexing import blacklist


def onions(args: List[str], onion_list={}, sema=None, session=networking.session_tor()) -> str:
    try:
        return misc.file_input(args)
    except:
        url = args.URL
    export = args.export if 'export' in args else ''
    output = args.output if 'output' in args else False
    onion_regex = re.compile('[A-Za-z0-9]+\.onion')
    host = urlparse(url).netloc

    my_onions = []
    print('Fetching onion websites from', url)
    try:
        page = session.get(url, timeout=30)
        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        for link in soup.find_all('a', href=True):
            if onion_regex.search(link['href']):
                if host not in link['href']:
                    my_onions.append(
                        onion_regex.search(link['href']).group(0))

        for link in soup(text=onion_regex):
            if host not in link:
                my_onions.append(onion_regex.search(link).group(0))

        my_onions = re.findall('[A-Za-z0-9]+\.onion', page.text, re.IGNORECASE)

    except Exception:
        if sema:
            sema.release()
        return ''

    not_blacklisted: List[str] = []
    blacklisted_onionv2: List[str] = []

    for link in my_onions:
        # Add the URL to the blacklist if onionv2
        if blacklist.check(url=link):
            blacklisted_onionv2.append(link)
        # Accept the URL
        else:
            not_blacklisted.append(link)

    not_blacklisted = ["http://" + (o[:-1] if o[-1] == "/" else o) for o in set(not_blacklisted)]

    if not output:
        # Saving onions
        uncrawled = []
        for o in not_blacklisted:
            uncrawled.append({
                'site': o,
                'indexers': [url]
            })
        database.save_uncrawled(uncrawled)

        # Saving onionv2 blacklisted onions
        uncrawled = []
        for o in blacklisted_onionv2:
            uncrawled.append({
                'site': o,
                'indexers': [url]
            })
        database.save_blacklisted(uncrawled, "onionV2")

    if export:
        handle_export.simple(not_blacklisted, export)

    onion_list[url] = not_blacklisted
    if sema:
        sema.release()
    return "\n".join(not_blacklisted)
