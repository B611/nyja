import re
from typing import List, Dict
import bs4
import yaml
import glob
import os


def match_in_soup(soup: bs4.BeautifulSoup, matches: List[str]) -> bool:
    [script.extract() for script in soup(["script", "style"])]
    matches = ["\\" + "b" + word + "\\" + "b" for word in matches]
    return True if re.search("|".join(matches), soup.get_text(), re.IGNORECASE) else False


def list_in_soup(soup: bs4.BeautifulSoup, matches: List[str]) -> List[str]:
    [script.extract() for script in soup(["script", "style"])]
    return list(set(re.findall("|".join(matches), soup.get_text().lower(), re.IGNORECASE)))


def check_login(soup: bs4.BeautifulSoup) -> bool:
    words = ["login", "log in", "register", "sign up", "signup"]
    return match_in_soup(soup, words)


def check_captcha(soup: bs4.BeautifulSoup) -> bool:
    words = ["captcha", "robot checker", "click on the broken circle", "are you human", "Anti-DDOS"]
    return match_in_soup(soup, words)


def check_cryptos(soup: bs4.BeautifulSoup) -> List[str]:
    cryptos = []

    with open("/app/resources/cryptos.yaml") as file:
        product_dict = yaml.safe_load(file)

    for crypto_name, crypto_matches in product_dict.items():
        cryptos.append(crypto_name) if match_in_soup(soup, crypto_matches) else None

    return cryptos


def check_products(soup: bs4.BeautifulSoup) -> Dict[str, List[str]]:
    configfiles = glob.glob("/app/resources/products/*.yaml")
    all_products = {}

    for configfile in configfiles:
        with open(configfile) as file:
            product_dict = yaml.safe_load(file)

        products = []
        for product_name, product_matches in product_dict.items():
            products.append(product_name) if match_in_soup(soup, product_matches) else None
        all_products[os.path.basename(configfile)[:-5]] = products

    return all_products
