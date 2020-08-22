# RUNNING ARGS python3 main.py fisier.txt

from mauFileHandler import *
from mauObjective import *
from mauSpyder import *

from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import requests


def main():
    #f.write(getWikiPage("Delta Dunarii"))
    #f.write(getWikiPage("dsadsadsasdasdaas"))

    objectives = readInputFile()
    for inputName in objectives:
        objective = Objective(inputName)
        soup = getWikiPage(inputName)
        printLog(inputName + " -> " + str(isPageValid(soup)))

    closeFiles()

if __name__ == "__main__":
    main()