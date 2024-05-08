#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
import json
import pandas as pd
from pprint import pprint

BASEPATH = os.path.dirname(os.path.abspath(__file__))

def bibleExcel2Dict(newTestmentDF):
    newTestmentDICT = {}

    for i in range(len(newTestmentDF["英文卷名"])):
        newTestmentDICT[newTestmentDF["英文卷名"].iloc[i].replace(" ", "")] = {
            "chinese_name": newTestmentDF["中文卷名"].iloc[i],
            "chinese_abbr": newTestmentDF["中文縮寫"].iloc[i],
            "english_abbr": newTestmentDF["英文縮寫"].iloc[i],
        }

    return newTestmentDICT


if __name__ == "__main__":

    newTestmentDF = pd.read_excel("bible_name.xlsx", sheet_name="new_testment")
    oldTestmentDF = pd.read_excel("bible_name.xlsx", sheet_name="old_testment")

    newTestmentDICT = bibleExcel2Dict(newTestmentDF)
    pprint(newTestmentDICT)
    with open(f"{BASEPATH}/newTestmentDICT.json", "w", encoding="UTF-8") as f:
        json.dump(newTestmentDICT, f, ensure_ascii=False, indent=4)

    oldTestmentDICT = bibleExcel2Dict(oldTestmentDF)
    pprint(oldTestmentDICT)


    with open(f"{BASEPATH}/oldTestmentDICT.json", "w", encoding="UTF-8") as f:
        json.dump(oldTestmentDICT, f, ensure_ascii=False, indent=4)
