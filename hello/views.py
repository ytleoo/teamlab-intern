from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

import json
import random
import requests
import MySQLdb
import random
#アドレスの末尾が/helloのときindexを実行
def index(request):
    return HttpResponse("Hello, World")


REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
#ACCESS_TOKEN =
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
}

def reply_text(reply_token, text):
    payload = {
          "replyToken":reply_token,
          "messages":[
                {
                    "type":"text",
                    "text": text
                }
            ]
    }

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload)) # LINEにデータを送信
    return reply

def reply_sticker(reply_token, p_Id, s_Id):
    payload = {
          "replyToken":reply_token,
          "messages":[
                {
                    "type":"sticker",
                    "packageId": p_Id,
                    "stickerId": s_Id
                }
            ]
    }

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload)) # LINEにデータを送信
    return reply

def callback(request):
    reply = ""
    request_json = json.loads(request.body.decode('utf-8')) # requestの情報をdict形式で取得
    for e in request_json['events']:
        reply_token = e['replyToken']  # 返信先トークンの取得
        message_type = e['message']['type']   # typeの取得

        if message_type == 'text':
            text = e['message']['text']    # 受信メッセージの取得
            reply += reply_text(reply_token, text)   # LINEにセリフを送信する関数
        elif message_type == 'sticker':
            p_Id = e['message']['packageId']
            s_Id = e['message']['stickerId']
            reply += reply_sticker(reply_token, p_Id, s_Id)   # LINEにセリフを送信する関数

    return HttpResponse(reply)  # テスト用

def teacher(teacher_name):
    
    connection = MySQLdb.connect()
    cursor = connection.cursor()
    cursor.execute('SELECT*FROM tbl_teacher')
    columns=['性格','イメージ','授業','評価','情報']
    result = cursor.fetchall()
    id=random.randint(2,6)

    for row in result:
        if row[1]==teacher_name:
            return (columns[id-2]+":"+row[id])
    return "そのような先生はいません"

