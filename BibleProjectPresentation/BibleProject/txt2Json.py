#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
import json
import re
from pprint import pprint

BASEPATH = os.path.dirname(os.path.abspath(__file__))

versePAT = re.compile("\d+:\d.+")
newTestmentNamePAT = re.compile("\d+.([^ ]+)\((.+)\)")
oldTestmentNamePAT = re.compile("(\d+)?\s?[A-z]+")

newTestmentDICT = json.load(open("newTestmentDICT.json"))
oldTestmentDICT = json.load(open("oldTestmentDICT.json"))

def organizedVerse(profileSTR):
    #把 txt 分開

    textLIST = profileSTR.split("\n")

    #變成 dictionary
    verseDICT = {}
    for text in textLIST:
        if versePAT.search(text):
            verseText = text.split(":")
            try:
                verseDICT[verseText[0]].append(verseText[1])
            except:
                verseDICT[verseText[0]] = [verseText[1]]

    return verseDICT

def saveOrganizedBible(bible_book):
    newFileNameLIST = os.listdir(f"{BASEPATH}/BibleData/{bible_book}/")

    for name in newFileNameLIST:
        if name.startswith("."):
            continue
        with open(f"{BASEPATH}/BibleData/{bible_book}/{name}", encoding="UTF-8") as f:
            fileSTR = f.read()

        result = organizedVerse(fileSTR)
        if bible_book == "newTestment":
            parsedName = newTestmentNamePAT.search(name).group(2).replace(" ", "")
        else:
            parsedName = oldTestmentNamePAT.search(name).group().replace(" ", "")

        with open(f"{BASEPATH}/BibleData/{bible_book}_organized/{parsedName}.json", "w", encoding="UTF-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)



if __name__ == "__main__":

    saveOrganizedBible("oldTestment")









    #存成 json