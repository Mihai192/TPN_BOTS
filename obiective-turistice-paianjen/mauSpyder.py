import requests
from robobrowser import RoboBrowser

from mauConstants import *

session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0'
browser = RoboBrowser(parser="html5lib", session=session)

def getWikiPage(inputString):
    data = "search=" + inputString
    browser.open(postURL, method="post", data=data)
    return str(browser.parsed)