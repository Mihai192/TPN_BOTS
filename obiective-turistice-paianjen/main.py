# RUNNING ARGS python3 main.py fisier.txt
from classes.dbCity import DBCity
from classes.dbOutput import DBOutput
from classes.objective import *
from config.functions import c_print
from fileHandler import *
from spyder import *

import time
import queue

db_city_conn = DBCity().connect()
db_output_conn = DBOutput().connect()
start_time = time.time()

def main():
    #f.write(getWikiPage("Delta Dunarii"))
    #f.write(getWikiPage("dsadsadsasdasdaas"))

    delayed_obj = queue.Queue()
    objectives = readInputFile()

    t_file = len(objectives)
    t_inserted = 0
    t_duplicate = 0

    c_print("[SPIDER]: In fisier sunt: " + str(t_file) + " obiective.")
    for inputName in objectives:
        objective = Objective(inputName)
        objective.soup = getWikiPage(inputName)
        objective.is_Valid = isPageValid(objective.soup)
        if objective.is_Valid == 2:
            delayed_obj.put(objective)
            b_print("[Warning]: " + inputName + " nu a fost gasit din prima, aman procesarea...")
        elif objective.is_Valid == 1:
            result = processWikiPage(objective.soup, objective.title)
            objective.clone(result)
            if objective.insertToDB() is True:
                t_inserted = t_inserted + 1
            else:
                t_duplicate = t_duplicate + 1
    c_print("[SPIDER]: " + str(t_inserted) + " obiective noi inserate. [" + str(t_duplicate) + " dubluri gasite]")
    c_print("[SPIDER]: Time executie - " + str(round(time.time() - start_time, 2)) + "s")

    closeFiles()

def temp():
    readTempFile()

if __name__ == "__main__":
    main()
    #temp()