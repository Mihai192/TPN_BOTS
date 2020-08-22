# RUNNING ARGS python3 main.py fisier.txt
from classes.dbCity import DBCity
from fileHandler import *
from classes.objective import *
from spyder import *

import queue

db_city_conn = DBCity().connect()

def main():
    #f.write(getWikiPage("Delta Dunarii"))
    #f.write(getWikiPage("dsadsadsasdasdaas"))

    delayed_obj = queue.Queue()
    objectives = readInputFile()

    for inputName in objectives:
        objective = Objective(inputName)
        objective.soup = getWikiPage(inputName)
        objective.is_Valid = isPageValid(objective.soup)
        if objective.is_Valid == 2:
            delayed_obj.put(objective)
        elif objective.is_Valid == 1:
            processWikiPage(objective.soup, objective.title)

    closeFiles()

if __name__ == "__main__":
    main()