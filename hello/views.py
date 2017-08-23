# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

import json
import random
import requests
import MySQLdb
from natto import MeCab


# アドレスの末尾が/helloのときindexを実行
def index(request):
    # return HttpResponse("Hello, World")
    return HttpResponse(teacher("鈴木先生"))


REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
# ACCESS_TOKEN ="アクセストークンの入力"

HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
}


def reply_text(reply_token, text):
    payload = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload))  # LINEにデータを送信
    return reply


def reply_sticker(reply_token, p_Id, s_Id):
    payload = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "sticker",
                "packageId": p_Id,
                "stickerId": s_Id
            }
        ]
    }

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload))  # LINEにデータを送信
    return reply


def callback(request_json):
    reply = ""
    request_json = json.loads(request.body.decode('utf-8'))  # requestの情報をdict形式で取得
    for e in request_json['events']:
        reply_token = e['replyToken']  # 返信先トークンの取得
        message_type = e['message']['type']  # typeの取得

        # if message_type == 'text':
        #     text = e['message']['text']    # 受信メッセージの取得
        #     reply += reply_text(reply_token, text)   # LINEにセリフを送信する関数
        if message_type == 'text':
            text = e['message']['text']  # 受信メッセージの取得

            reply += reply_text(reply_token, select_data(text))  # LINEにセリフを送信する関数
        # reply += reply_text(reply_token, teacher(text))   # LINEにセリフを送信する関数

        elif message_type == 'sticker':
            p_Id = e['message']['packageId']
            s_Id = e['message']['stickerId']
            if 1 <= int(p_Id) <= 4:
                reply += reply_sticker(reply_token, p_Id, s_Id)  # LINEにセリフを送信する関数
            else:
                reply += reply_text(reply_token, "www")  # LINEにセリフを送信する関数
                # reply += reply_sticker(reply_token, p_Id, s_Id)   # LINEにセリフを送信する関数

    return HttpResponse(reply)  # テスト用

#フォローされたときにfirstfollowを実行
def firstfollow(request_json):#requestの情報をdict形式で受け取る
    emoji = {"happy":"0x100001", "ok":"0x100033", "yes":"0x1000A5", "love":"0x100078"}  #emojiのunicodeを格納
    thank = "さつまいも大学スイートポテト学部の裏シラバスへようこそ"+chr(emoji["yes"])
    +"\n僕が先生や授業について様々な情報をおしえてあげるよ"+chr(emoji["ok"])
    +"\n気軽に話しかけてみてね"+chr(emoji["love"])
    reply = ""
    #request_json = json.loads(request.body.decode('utf-8'))  # requestの情報をdict形式で取得
    for e in request_json['events']:
        reply_token = e['replyToken']   #返信先トークンの取得
        reply += reply_text(reply_token, thank)
    return HttpResponse(reply)

def main(request):
    request_json = json.loads(request.body.decode('utf-8'))  # requestの情報をdict形式で取得
    for e in request_json['events']:
        event_type = e['type']
        if event_type == "message":#スタンプやメッセージを受け取ったとき
            callback(request_json)
        elif event_type == "follow":#フォローされたとき
            firstfollow(request_json)


def select_data(text):
    mc = MeCab()
    words = []
    with MeCab('-F%m,%f[0],%h') as nm:
        for n in nm.parse(text, as_nodes=True):
            node = n.feature.split(',');
            if len(node) != 3:
                continue
            if node[1] == '名詞':
                words.append(node[0])
    # print(words) #wordsに名刺の単語のみのリストが格納

    if len(words) >= 2 and (words[1] == '先生' or words[1] == 'せんせい'):
        return teacher(words[0] + "先生")
    else:
        if len(words) == 1:
            tmp = words[0]
        elif len(words) == 2:
            tmp = words[0] + words[1]
        elif len(words) == 3:
            tmp = words[0] + words[1] + words[2]
        else:
            for i in range(words):
                tmp = tmp + words[i]
        return Class(tmp)


def teacher(teacher_name):
    # connection = MySQLdb.connect(host, user, passwd,etc.)
    cursor = connection.cursor()
    cursor.execute('SELECT*FROM tbl_teacher')
    columns = ['性格', '特徴', '担当授業', '総合評価', '裏情報', '裏情報２']
    musubi = ['です。', 'だよ。', 'の授業を担当しています。', 'だよ。', 'らしいよ。', 'らしいよ']
    result = cursor.fetchall()

    for row in result:
        id = random.randint(2, len(row) - 1)
        if row[1] == teacher_name:
            if id == 5:
                return (teacher_name + 'の評価は' + "☆" * int(row[id]) + musubi[id - 2])
            else:
                return (teacher_name + 'は' + row[id] + musubi[id - 2])
            return (teacher_name + "は今学校にはいないよ")


def Class(class_name):
    # connection = MySQLdb.connect(host, user, passwd,etc.)
    cursor = connection.cursor()
    cursor.execute('SELECT*FROM tbl_class')
    columns = ['単位期待度', '成績評価方法', 'ためになる度']
    result = cursor.fetchall()
    for row in result:
        id = random.randint(2, len(row) - 1)
        if row[1] == class_name:
            return (class_name + "の" + columns[id - 2] + "は" + row[id] + "だよ。")
    return class_name + "は登録されていないよ"


def teacher(teacher_name):
    connection = MySQLdb.connect()  # host, user,passwd,etc.
    cursor = connection.cursor()
    cursor.execute('SELECT*FROM tbl_teacher')
    columns = ['性格', 'イメージ', '授業', '評価', '情報']
    result = cursor.fetchall()
    id = random.randint(2, 6)

    for row in result:
        if row[1] == teacher_name:
            return (columns[id - 2] + ":" + str(row[id]))
    return "そのような先生はいません"