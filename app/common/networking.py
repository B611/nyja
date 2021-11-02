import os, requests, random
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def get_random_user_agent() -> str:
    origin: str = "/app/resources/user-agents/"
    fname: str = random.choice(os.listdir(origin))
    with open(origin + fname, "r") as f:
        return random.choice(f.read().splitlines())


def session_tor() -> requests.Session:
    session: requests.Session = requests.session()
    tor_proxy: str = os.environ['TOR_PROXY']
    session.proxies = {'http': 'socks5h://' + tor_proxy,
                       'https': 'socks5h://' + tor_proxy}
    session.headers.update({'User-Agent': get_random_user_agent()})
    return session


def session_clearweb() -> requests.Session:
    session: requests.Session = requests.session()
    session.headers.update({'User-Agent': get_random_user_agent()})

    return session
