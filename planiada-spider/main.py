from config.constants import counties
from classes.pln_county import pCounty
from config.functions import c_print

def main():
    for idx, cName in enumerate(counties):
        county = pCounty(idx + 1, cName)
        c_print("[# " + str(idx) + "/" + str(len(counties)) + "] Analizez judetul " + str(cName))
        county.process()
        if idx is 1:
            exit()

if __name__ == "__main__":
    main()
