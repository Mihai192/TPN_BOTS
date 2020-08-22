from config.constants import *

def q_print(string):
    if debug >= 1 and defaultStream is "console":
        print(string)

def m_print(string):
    if debug is 1 and defaultStream is "console":
        print(string)