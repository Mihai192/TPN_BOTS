import sys

inputObjectives = []

def readInputFile():
    inputPath = str(sys.argv[1])
    with open(inputPath) as inputFile:
        for line in inputFile:
            inputObjectives.append(line)
    return inputObjectives