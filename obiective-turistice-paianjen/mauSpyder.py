from mauConstants import *

import requests
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser

session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0'
browser = RoboBrowser(parser="html5lib", session=session)

def isPageValid(soup):
    canonical = str(soup.find('link', {'rel': 'canonical'}))
    if "https://ro.wikipedia.org/wiki/w/" in canonical:
        return False
    else:
        return True

def getWikiPage(inputString):
    data = {'search': inputString}
    response = requests.post(postURL, data=data)
    bsoup = BeautifulSoup(response.text, "html5lib")
    return bsoup