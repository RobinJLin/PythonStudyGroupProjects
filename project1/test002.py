#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
import json

BASEPATH = os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":


    # 輸入
    gender: str = input("請輸入性別(男/女):")
    age: int = int(input("請輸入年齡："))
    height: float = float(input("請輸入身高(公分)："))
    weight: float = float(input("請輸入體重(公斤)："))
    bodyFat: float = float(input("請輸入體脂率(百分比)："))
    print("""
    活動因子參考數值
    無活動：1.2
    輕度活動：1.375
    中度活動：1.55
    高度活動：1.725
    非常高度活動：1.9
    """)
    activeFactor: float = float(input("請輸入活動因子(請填數字)："))
    print("""
    壓力因子參考數值
    正常：1.0
    發燒：1.13
    小手術、癌症：1.2
    骨骼受傷：1.3
    癌症惡質病：1.4
    懷孕：1.1
    哺乳：1.4
    生長期：1.4
    """)
    pressureFactor: float = float(input("請輸入壓力因子(請填數字)："))

    #計算 BMI
    bmi: float = weight / (height / 100)**2

    #判斷 體重狀態
    if bmi < 18.5:
        bmiStatus: str = "體重過輕"
    elif 18.5 <= bmi < 24:
        bmiStatus = "正常"
    elif 24 <= bmi < 27:
        bmiStatus = "過重"
    elif 27 <= bmi < 30:
        bmiStatus = "輕度肥胖"
    elif 30 <= bmi < 35:
        bmiStatus = "中度肥胖"
    else:
        bmiStatus = "重度肥胖"

    #計算 除脂體重
    nonFatWeight: float = weight*(100 - bodyFat) / 100

    #計算 基礎代謝率
    if "男" in gender:
        bmr: float = 66 + (13.7*weight + 5 * height - 6.8 * age)
    elif "女" in gender:
        bmr: float = 65 + (9.6*weight + 1.8 * height - 4.7 * age)
    else:
        print("輸入錯誤，請再輸入一次")


    #計算 TDEE
    TDEE = bmr * activeFactor * pressureFactor
    carbohydrate: float = ((TDEE * 20) / 4) / 100
    protein: float = ((TDEE * 30) / 4) / 100
    fat: float = ((TDEE * 50) / 9) / 100

    print("#-----您的健康飲食報告----#")

    print("您的BMI為：{}".format(bmi))
    print("您的除脂體重為：{}".format(nonFatWeight))
    print("您的體重狀態為：{}".format(bmiStatus))
    print("您的體脂率為：{}".format(bodyFat))
    print("您的基礎代謝率：{}".format(bmr))
    print("您的熱量總消耗為：{}".format(TDEE))
    print("您的低碳飲食法三大營養素建議克數為：")
    print("碳水化合物：{} 克".format(carbohydrate))
    print("蛋白質：{} 克".format(protein))
    print("脂肪：{} 克".format(fat))
