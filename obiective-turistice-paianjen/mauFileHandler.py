import sys

inputObjectives = []

consoleFile = open("log_console.txt", "a")

def printLog(string):
    consoleFile.write(string + "\n")
    print(string)

def closeFiles():
    consoleFile.close()

def readInputFile():
    inputPath = str(sys.argv[1])
    with open(inputPath) as inputFile:
        for line in inputFile:
            inputObjectives.append(line.rstrip())
    return inputObjectives