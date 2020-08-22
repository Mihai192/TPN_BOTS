import sys

import bs4

inputObjectives = []

consoleFile = open("log_console.txt", "w", encoding='utf-8')

def printLog(string):
    consoleFile.write(string + "\n")

def closeFiles():
    consoleFile.close()

def readInputFile():
    inputPath = str(sys.argv[1])
    with open(inputPath, "r", encoding='utf-8') as inputFile:
        for line in inputFile:
            inputObjectives.append(line.rstrip())
    return inputObjectives

def readTempFile():
    inputPath = "temp.txt"
    with open(inputPath, "r") as inputFile:
        soup = bs4.BeautifulSoup(inputFile, 'html.parser')
        soup_elements = soup.findAll('td', {"class":"denumire"})
        for elem in soup_elements:
            soup_el = elem.find('span')
            if soup_el is not None:
                outTitle = soup_el.text
                begin_idx = outTitle.find('.')
                outTitle = outTitle[begin_idx + 1:].lstrip()
                print(outTitle)

