#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
import json
from email import header
from pprint import pprint

import pandas as pd
from PIL import ImageColor
from xml.etree import ElementTree as ET


BASEPATH = os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":

    # 讀檔-整理內容-存檔
    pathSTR = f"{BASEPATH}/總統-各投票所得票明細及概況(Excel檔)/總統-A05-1-候選人得票數一覽表(中　央).xlsx"

    dataframe1 = pd.read_excel(pathSTR, header=None)

    place = dataframe1[0][5:]
    preprocessed_place = []
    for p in place:
        preprocessed_place.append(p.replace("\u3000", ""))

    tpp_data = dataframe1[1][5:]
    dpp_data = dataframe1[2][5:]
    kmt_data = dataframe1[3][5:]

    tpp = dict(zip(preprocessed_place, tpp_data))
    dpp = dict(zip(preprocessed_place, dpp_data))
    kmt = dict(zip(preprocessed_place, kmt_data))

    voting_json = {
        "tpp":tpp,
        "dpp":dpp,
        "kmt":kmt
    }

    with open(f"{BASEPATH}/voting_results.json", "w", encoding="UTF-8") as f:
        json.dump(voting_json, f, ensure_ascii=False, indent=4)


    ## 重新整理檔案，key 為 location
    with open("voting_results.json", "r", encoding="utf-8") as file:
        voting_results = json.load(file)

    locationDICT = {}
    for result in voting_results:
        for location in voting_results[result]:
            locationDICT[location] = {}

    for location in locationDICT:
        locationDICT[location] = {"tpp": voting_results["tpp"][location],
                                  "dpp": voting_results["dpp"][location],
                                  "kmt": voting_results["kmt"][location]
                                  }

    pprint(locationDICT)

    ## percentage

    percentage = {}
    for location in locationDICT:
        location_sum = sum(locationDICT[location].values())
        percentage[location] = {"tpp": (locationDICT[location]["tpp"]/location_sum )*100, "dpp": (locationDICT[location]["dpp"]/location_sum)*100, "kmt": (locationDICT[location]["kmt"]/location_sum)*100}

    pprint(percentage)

    ## 計算 winner 和 得票差距

    diff_list = []
    for location in percentage:
        result = sorted(percentage[location].items(), key=lambda x:x[1], reverse=True)
        diff = result[0][1] - result[1][1]
        diff_list.append(diff)
        print(f"{location} 獲勝者: {result[0][0]}, 與第二名的得票差距: {round(diff, 2)}%")

    max_ticket_diff = round(max(diff_list), 2)
    print(f"最大的得票差距: {round(max(diff_list), 2)}%")

    ## 色彩漸層設定

    for location in percentage:
        result = sorted(percentage[location].items(), key=lambda x:x[1], reverse=True)
        diff = result[0][1] - result[1][1]
        diff_list.append(diff)
        print(f"{location} 獲勝者: {result[0][0]}, 與第二名的得票差距: {round(diff, 2)}%")
        ratio = round(diff, 2) / max_ticket_diff
        if result[0][0] == "dpp":
            print(f"HSL: hsl(130, 60%, {int(75 - 40 *ratio)}%)")
        if result[0][0] == "kmt":
            print(f"HSL: hsl(212, 100%, {int(75 - 40 *ratio)}%)")
        if result[0][0] == "tpp":
            print(f"HSL: hsl(177, 61%, {int(85 - 40 *ratio)}%)")

    ## 轉換成 HEX 色碼
    colors = {}
    for location in percentage:
        print(location)
        result = sorted(percentage[location].items(), key=lambda x:x[1], reverse=True)
        diff = result[0][1] - result[1][1]
        diff_list.append(diff)
        print(f"{location} 獲勝者: {result[0][0]}, 與第二名的得票差距: {round(diff, 2)}%")
        ratio = round(diff, 2) / max_ticket_diff

        if result[0][0] == "dpp":
            color = ImageColor.getrgb(f"hsl(130, 60%, {int(75 -40 *ratio)}%)")
            r = color[0]
            g = color[1]
            b = color[2]
            colors[location] = f"#{r:02x}{g:x}{b:x}"

        if result[0][0] == "kmt":
            color = ImageColor.getrgb(f"hsl(212, 100%, {int(75 -40 *ratio)}%)")
            print(color)
            r = color[0]
            g = color[1]
            b = color[2]
            colors[location] = f"#{r:02x}{g:x}{b:x}"

        if result[0][0] == "tpp":
            color = ImageColor.getrgb(f"hsl(177, 61%, {int(75 -40 *ratio)}%)")
            r = color[0]
            g = color[1]
            b = color[2]
            colors[location] = f"#{r:02x}{g:x}{b:x}"
    pprint(colors)

    # 開啟 SVG 檔案
    file_path = f"Blank_Taiwan_map.svg"  # 上傳的檔案路徑
    with open(file_path, "r", encoding="UTF-8") as file:
        svg_content = file.read()

    # 開啟 SVG 檔案
    file_path = "Blank_Taiwan_map.svg"  # 上傳的檔案路徑
    with open(file_path, "r", encoding="UTF-8") as file:
        svg_content = file.read()

    # 解析SVG內容
    svg_tree = ET.fromstring(svg_content)

    # 尋找所有 <path> 元素，檢查其 <title> 子元素是否匹配指定的縣市名稱
    for path in svg_tree.iterfind(".//{http://www.w3.org/2000/svg}path"):
        print(path)
        title = path.find("{http://www.w3.org/2000/svg}title")

        # 問題：title 都是 none 可以怎麼改
        if title is not None:
            target = title.text.strip().split(" ")[0]
            path.set("fill", colors[target])

    # 如果成功修改，則保存修改後的SVG內容到一個新檔案
    modified_svg_path = "Modified_Taiwan_map.svg"
    ET.ElementTree(svg_tree).write(modified_svg_path, encoding="utf-8")

    # 顯示成功訊息
    print(f"修改成功! SVG 檔已存於 {modified_svg_path}")
