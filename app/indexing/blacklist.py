import yaml
import common.database as database


def check(url: str = "", title: str = "", offline_check: str = "") -> bool:
    if offline_check:
        if database.ban_offline_check(offline_check):
            return True
    if url:
        if not check_onionv3(url):
            return True
    if title:
        if check_blacklisted(title):
            return True
    return False


def check_onionv3(url: str) -> bool:
    if url.startswith("http://"):
        url = url[7:]
    # In onion V3: 56 character URL + ".onion"
    # And last character of URL is always "d"
    return len(url.split("/")[0]) == 62 and url[55] == "d"


def check_blacklisted(content: str):
    content = content.lower()
    with open("/app/resources/blacklist.yaml") as file:
        banned_words_dict = yaml.safe_load(file)

    for banned_category, banned_words in banned_words_dict.items():
        for banned_word in banned_words:
            if banned_word in content:
                return True

    return False
