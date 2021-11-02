import random
import magic
import base64
import urllib


def check_extension(favrequest):
    magik = magic.from_buffer(favrequest.content, mime=True)

    if magik == "image/vnd.microsoft.icon":
        icontype = "ico"
    elif magik.startswith("image/"):
        icontype = magik.split("/")[-1]
    else:
        icontype = ""
    return icontype


def fetch(session, url, soup):
    # SCENARIO 1 : IMAGE IN /FAVICON.ICO UR
    icon, icontype = get_ico(session, url)

    # SCENARIO 2 : NO FAVICON.ICO, LINK TO IMAGE IN HTML
    # WARNING
    # POTENTIALLY FETCHING SENSITIVE CONTENT, DO NOT ENABLE WHEN USING WITH UNKOWN INDEXERS

    # if not icon or not icontype:
    #     icon, icontype = get_html_image(session, soup, url)

    # WRITE ICONS AS FILE FOR MANUAL DEBUG
    # if icon and icontype:
    #     print(url, icontype)
    #     with open(str(random.randint(1, 1000000)) + "." + icontype, "wb") as f:
    #         f.write(icon)
    if icon:
        icon = base64.b64encode(icon).decode('utf-8')
    return icon, icontype
    # return base64.b64encode(icon.encode('utf-8')).decode('utf-8'), icontype


def get_ico(session, url):
    icon = ""
    icontype = ""

    try:
        url = urllib.parse.urlparse(url)
        try:
            favrequest = session.get(
                url.scheme + "://" + url.netloc + "/favicon.ico")
        except:
            favrequest = session.get(
                url.scheme + "://" + url.netloc + "/static/images/favicon.ico")
        if favrequest.status_code == 200:
            icontype = check_extension(favrequest)
            if icontype:
                icon = favrequest.content
    except Exception as e:

        # print(e)
        pass

    return icon, icontype


def get_html_image(session, soup, url):
    icon = ""
    icontype = ""

    try:
        img_tags = soup.find_all('img')
        if len(img_tags) > 0:
            img_link = img_tags[0]['src']

            # Image is in base64
            if img_link.startswith("data:image/"):
                icontype = img_link[11:].split(";")[0]
                icon = base64.b64decode(img_link.split(",")[1])

            # Image in a link
            else:
                # If image is relative path
                if img_link.startswith("/"):
                    img_link = url + img_link
                iconrequest = session.get(img_link)
                if iconrequest.status_code == 200:
                    icontype = check_extension(iconrequest)
                    if icontype:
                        icon = iconrequest.content
    except Exception as e:
        # print(e)
        pass

    return icon, icontype
