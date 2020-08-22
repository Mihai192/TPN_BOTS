import re

from config.constants import *

from unidecode import unidecode

from fileHandler import printLog

non_url_safe = ['"', '#', '$', '%', '&', '+',
                ',', '/', ':', ';', '=', '?',
                '@', '[', '\\', ']', '^', '`',
                '{', '|', '}', '~', "'"]
translate_table = {ord(char): u'' for char in non_url_safe}


def build_slug(string):
    clean_string = unidecode(string.lower())
    text = clean_string.translate(translate_table)
    text = u'-'.join(text.split())
    return text

def c_print(string):
    if debug <= 3 and defaultStream is "console":
        print(string)
    printLog(string)

def b_print(string):
    if debug <= 2 and defaultStream is "console":
        print(string)
    printLog(string)

def a_print(string):
    if debug is 1 and defaultStream is "console":
        print(string)
    printLog(string)

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext