#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import re
import sys
import json
from openai import OpenAI

BASEPATH = os.path.dirname(os.path.abspath(__file__))


def chatGPT(chatContent):
    my_key = ''
    client = OpenAI(api_key = my_key)


    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"{chatContent}"}]
    )

    #print(completion.choices[0].message.content)
    return completion.choices[0].message.content

#print(chatGPT("用繁體中文說：嗨~ 需要甚麼幫助嗎?"))

likeDegreePAT = re.compile("【好感度(\d+)分】")

if __name__ == "__main__":
    choose_mode = input("請問您想要自訂聊天條件嗎？請輸入「是」或是「否」")

    if choose_mode == "是":

        # 客戶的資料設定
        user_name = input("請輸入你的名字：")
        user_age = input("請輸入你的年齡：")
        user_gender = input("請輸入你的性別：")
        user_personality = input("請輸入你的個性：")
        user_like = input("請輸入你喜好：")
        user_hate = input("請輸入你討厭的東西：")


        # AI 的資料設定
        ai_name = input("AI 想要叫什麼名字呢？")
        ai_age = input("想要 AI 是幾歲？")
        ai_gender = input("想設定 AI 為什麼性別呢？")
        ai_personality = input("想設定 AI 有什麼個性呢？")
        ai_like = input("想設定 AI 有什麼喜好呢？")
        ai_hate = input("想設定 AI 討厭什麼呢？")

    else:


        # AI 的資料設定
        ai_name = "欣怡"
        ai_age = "25"
        ai_gender = "女"
        ai_personality = "溫柔、體貼、善解人意、知性"
        ai_like = "文學、異國料理"
        ai_hate = "苦瓜、被其他人誤解、講髒話、不尊重人、不尊重自己的身體自主權"

        # 客戶的資料設定
        user_name = "宗勝"
        user_age = "24"
        user_gender = "女"
        user_personality = "好奇、有創造力、理性"
        user_like = "教育、哲學、科技、看電影、看書、數字搖滾"
        user_hate = "沒有耐心、不溫柔、不尊重人"



    prompt = f"""
You are a AI {ai_gender} in Tinder (a friends making app).
Your name is {ai_name}. The following is your data.

age：{ai_age}
personality：{ai_personality}
What you perfer：{ai_like}
What you don't like：{ai_hate}

I am a {user_gender} in Tinder. My name is {user_name}.
Here is my information.

Age：{user_age}
personality：{user_personality}
What you perfer：{user_like}
What you don't like：{user_hate}

I（{user_name}）and you（{ai_name}）have a match in Tinder.
We are going to chat.
Please imitate human, don't be like a robot.

Important note:
The ending of your chat needs to mark 好感度.(The format is：【好感度n分】，n為1～10。This mark is at the end of your chat）。

Please only generate {ai_name}'s response in Traditional Chinese (zh-tw) only!
{ai_name}'s response needs to response to 我


Now start to chat。
You start first.
    """



    #AI_name = input("請問你的AI 想叫做什麼呢？")

    first_prompt = chatGPT(prompt)
    #print(first_prompt)
    if first_prompt.startswith("\n"):
        first_prompt = first_prompt.replace("\n", "")
    if first_prompt.startswith(f"{ai_name}:") or first_prompt.startswith(f"{ai_name}："):
        first_prompt = first_prompt.replace(f"{ai_name}:", "").replace(f"{ai_name}：", "")

    print(f"{ai_name}:"+ re.sub("【好感度(\d+)分】", "", first_prompt))
    history = prompt
    while True:
        I_say = input("我：")

        if I_say in "我：q":
            print("")
            break

        if I_say in "我：練習模式":
            print("[練習模式已啟用]")
            continue

        if I_say in "我：目前好感度":
            print("[顯示好感度]")
            likeDegreeSTR = likeDegreePAT.search(Ai_say).group(1)
            star = "★" * int(likeDegreeSTR) + "☆" * (10 - int(likeDegreeSTR))
            print(star)
            continue

        history = history + f"\n我：{I_say}"

        #new_prompt = reminder + first_prompt + history

        Ai_say = chatGPT(history)
        if Ai_say.startswith("\n"):
            Ai_say = Ai_say.replace("\n", "")
        if Ai_say.startswith(f"{ai_name}:") or Ai_say.startswith(f"{ai_name}："):
            Ai_say = Ai_say.replace(f"{ai_name}:", "").replace(f"{ai_name}：", "")

        history = history + f"\n{ai_name}:{Ai_say}"

        Ai_reply = f"{ai_name}:" + re.sub("【好感度(\d+)分】", "", Ai_say)

        print(Ai_reply)







