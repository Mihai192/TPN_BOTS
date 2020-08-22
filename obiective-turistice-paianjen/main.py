# RUNNING ARGS python3 main.py fisier.txt

from mauFileHandler import readInputFile
from mauObjective import *
from mauSpyder import getWikiPage
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import requests

f = open("page.html", "a")


def main():
    f.write(getWikiPage("Delta Dunarii"))
    f.close()
    '''objectives = readInputFile()
    for inputName in objectives:
        objective = Objective(inputName)'''



if __name__ == "__main__":
    main()