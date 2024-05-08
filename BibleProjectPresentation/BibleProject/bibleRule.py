#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import datetime
import os
import re
from pprint import pprint
import sys
import json

BASEPATH = os.path.dirname(os.path.abspath(__file__))

newTestmentDICT = json.load(open(f"{BASEPATH}/newTestmentDICT.json"))
oldTestmentDICT = json.load(open(f"{BASEPATH}/oldTestmentDICT.json"))

bibleDICT = {}
bibleDICT.update(newTestmentDICT)
bibleDICT.update(oldTestmentDICT)

chapterPAT = re.compile("(\d+)-(\d+)")
oneChapterPAT = re.compile("(\d+)")
specialChatpterPAT = re.compile("(\d+):((\d+)(-(\d+))?)")

def getBibleText(inputSTR):
    chineseNameSTR = ""
    for key in bibleDICT:
        chineseAbbr = bibleDICT[key]["chinese_abbr"]
        if chineseAbbr in inputSTR:
            chineseNameSTR = bibleDICT[key]["chinese_name"]
            try:
                bibleTextDICT = json.load(open(f"{BASEPATH}/BibleData/bible/{key}.json"))
                pprint(bibleTextDICT)
            except:
                resultText = "你的縮寫是不是寫錯了呢？再檢查一下喔！"
                return resultText

    if any(x in inputSTR for x in [":", "："]):
        chapterINT = int(specialChatpterPAT.search(inputSTR).group(1))
        verseStartINT = int(specialChatpterPAT.search(inputSTR).group(3))
        verseEndINT = int(specialChatpterPAT.search(inputSTR).group(5))

        resultLIST = bibleTextDICT[str(chapterINT)][verseStartINT - 1:verseEndINT]
        resultSTR = "".join(resultLIST)
        resultText = f"""====={chineseNameSTR} {chapterINT}: {verseStartINT}-{verseEndINT} =====
        {resultSTR}

        """

    else:
        if "-" in inputSTR:
            chapterStartINT = int(chapterPAT.search(inputSTR).group(1))
            chapterEndINT = int(chapterPAT.search(inputSTR).group(2))
            try:
                resultLIST = []
                for i in range(chapterStartINT, chapterEndINT+1):
                    bibleText = "".join(bibleTextDICT[str(i)]).replace(" ", "")

                    resultText = f"""======={chineseNameSTR} {i}========
            {bibleText}
                    """
                    resultLIST.append(resultText)
                resultText = "".join(resultLIST)
            except:
                resultText = "章節數字是否有寫對呢？再檢查一下喔～"
        else:
            chapterStartINT = int(oneChapterPAT.search(inputSTR).group(1))
            try:
                resultLIST = []
                bibleText = "".join(bibleTextDICT[str(chapterStartINT)]).replace(" ", "")


                resultText = f"""======={chineseNameSTR} {chapterStartINT}========
            {bibleText}
                    """
                resultLIST.append(resultText)
                resultText = "".join(resultLIST)
            except:
                resultText = "章節數字是否有寫對呢？再檢查一下喔～"

    return resultText

def getTargetBible(inputSTR):
    inputLIST = inputSTR.split(",")

    resultTextLIST = []
    for target in inputLIST:
        resultTextLIST.append(getBibleText(target))

    resultSTR = "".join(resultTextLIST)
    return resultSTR

if __name__ == "__main__":

    # input: 撒下 8-10 詩 119:155-176


    # 縮寫轉成英文名字  數字 start-end
    inputSTR = "詩篇 119:67-88"

    inputSTR = "箴言 12"
    pprint(getTargetBible(inputSTR))












    # output 提出內容