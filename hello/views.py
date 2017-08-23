# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

import json
import random
import requests
import MySQLdb
from natto import MeCab

emoji = {"happy":0x100001, "ok":0x100033, "yes":0x1000A5, "love":0x100078, "pencil":0x100041}  #emojiのunicodeを格納


# アドレスの末尾が/helloのときindexを実行
def index(request):
    # return HttpResponse("Hello, World")
    return HttpResponse(teacher("鈴木先生"))

#LINE APIの設定
REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'

# ACCESS_TOKEN ="アクセストークン"

HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
}



#文字列を出力
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


#スタンプを出力
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

def main(request):
    request_json = json.loads(request.body.decode('utf-8'))  # requestの情報をdict形式で取得
    for e in request_json['events']:
        event_type = e['type']
        if event_type == "message":#スタンプやメッセージを受け取ったとき
            callback(request_json)
        elif event_type == "follow":#フォローされたとき
            firstfollow(request_json)

#ユーザによる入力の時
def callback(request_json):
    reply = ""
    #request_json = json.loads(request.body.decode('utf-8')) # requestの情報をdict形式で取得

    for e in request_json['events']:
        reply_token = e['replyToken']  # 返信先トークンの取得
        message_type = e['message']['type']  # typeの取得

        #テキストを受け取ったとき出力する内容に関するデータベースを選択するメソッド
        if message_type == 'text':

            text = e['message']['text']    # 受信メッセージの取得
            reply += reply_text(reply_token, select_data(text))   # LINEにセリフを送信する関数
        #スタンプを受け取った時の処理
        elif message_type == 'sticker':
            p_Id = e['message']['packageId']
            s_Id = e['message']['stickerId']
            #LINEに付属するデフォルトのスタンプのときオウム返し
            if 1 <= int(p_Id) <= 4:
                reply += reply_sticker(reply_token, p_Id, s_Id)   # LINEにセリフを送信する関数
            #デフォルト以外のスタンプの時、"www"を出力
            else:
                reply +=  reply_text(reply_token, "www")   # LINEにセリフを送信する関数
    return HttpResponse(reply)  # テスト用

#フォローされた時
def firstfollow(request_json):#requestの情報をdict形式で受け取る
    global emoji
    thank = 'さつまいも大学スイートポテト学部の裏シラバスへようこそ'+chr(emoji["yes"])+'\n僕が先生や授業について様々な情報をおしえてあげるよ'+chr(emoji["ok"])+'\n気軽に話しかけてみてね'+chr(emoji["love"])
    reply = ""
    for e in request_json['events']:
        reply_token = e['replyToken']   #返信先トークンの取得
        reply += reply_text(reply_token, thank)
    return HttpResponse(reply)


def select_data(text):
    mc = MeCab()
    words = []
    #受け取った文より名詞のみを抽出→リストへ
    with MeCab('-F%m,%f[0],%h') as nm:
        for n in nm.parse(text, as_nodes=True):
            node = n.feature.split(',');
            if len(node) != 3:
                continue
            if node[1] == '名詞':
                words.append(node[0])

    #[〇〇,先生]というリストを受け取ったとき
    if len(words) >= 2 and (words[1] == '先生' or words[1] == 'せんせい'):
        if len(words) ==2:
            return teacher(words[0])
        elif len(words) ==3:
            for ps in range(len(words)):
                if words[ps] == '人' or words[ps] == 'ひと':
                    return teacher(words[0])
            return teacher(words[0],words[2])
        elif len(words) ==4:
            return teacher(words[0],words[2]+words[3])
    #授業科目名が入っているリストを受け取ったとき
    else:
        tmp = '0'
        flag=0
        if len(words) == 1:
            tmp = words[0]
            return Class(tmp)

        elif len(words) == 2:
            #一つが科目名、もう一つが特徴の時
            tmp = words[0]
            cursor = connection.cursor()
            cursor.execute('SELECT class FROM tbl_class')
            result = cursor.fetchall()
            for cs in range(len(result)):
                if tmp == result[cs][0]:
                    tmp2 = words[1]
                    return Class(tmp,tmp2)
            #二つ合わせて科目名のとき
            tmp = words[0]+words[1]
            return Class(tmp)

        elif len(words) == 3:
            tmp = words[0]
            cursor = connection.cursor()
            cursor.execute('SELECT class FROM tbl_class')
            result = cursor.fetchall()
            for cs in range(len(result)):
                if tmp == result[cs][0]:
                    tmp2 = words[1]
                    for wo in range(2,len(words)):
                        tmp2 = tmp2 + words[wo]
                    return Class(tmp,tmp2)
            tmp = words[0]+words[1]
            num=2
            cursor = connection.cursor()
            cursor.execute('SELECT class FROM tbl_class')
            result = cursor.fetchall()
            for cs in range(len(result)):
                if tmp == result[cs][0]:
                    tmp2 = words[num]
                    return Class(tmp,tmp2)
            tmp = words[0]+words[1]+words[2]
            return Class(tmp)

        elif len(words) == 4:
            tmp = words[0]
            cursor = connection.cursor()
            cursor.execute('SELECT class FROM tbl_class')
            result = cursor.fetchall()
            for cs in range(len(result)):
                if tmp == result[cs][0]:
                    tmp2 = words[1]
                    for wo in range(2,len(words)):
                        tmp2 = tmp2 + words[wo]
                    return Class(tmp,tmp2)
            tmp = words[0]+words[1]
            num=2
            cursor = connection.cursor()
            cursor.execute('SELECT class FROM tbl_class')
            result = cursor.fetchall()
            for cs in range(len(result)):
                if tmp == result[cs][0]:
                    tmp2 = words[num]
                    for wo in range(num+1,len(words)):
                        tmp2 = tmp2 + words[wo]
                    return Class(tmp,tmp2)
            tmp = words[0]+words[1]+words[2]
            num=3
            cursor = connection.cursor()
            cursor.execute('SELECT class FROM tbl_class')
            result = cursor.fetchall()
            for cs in range(len(result)):
                if tmp == result[cs][0]:
                    tmp2 = words[num]
                    return Class(tmp,tmp2)
            tmp = words[0]+words[1]+words[2]+words[3]
            return Class(tmp)

        elif len(words) == 5:
            tmp = words[0]
            cursor = connection.cursor()
            cursor.execute('SELECT class FROM tbl_class')
            result = cursor.fetchall()
            for cs in range(len(result)):
                if tmp == result[cs][0]:
                    tmp2 = words[1]
                    for wo in range(2,len(words)):
                        tmp2 = tmp2 + words[wo]
                    return Class(tmp,tmp2)
            tmp = words[0]+words[1]
            num=2
            cursor = connection.cursor()
            cursor.execute('SELECT class FROM tbl_class')
            result = cursor.fetchall()
            for cs in range(len(result)):
                if tmp == result[cs][0]:
                    tmp2 = words[num]
                    for wo in range(num+1,len(words)):
                        tmp2 = tmp2 + words[wo]
                    return Class(tmp,tmp2)
            tmp = words[0]+words[1]+words[2]
            num=3
            cursor = connection.cursor()
            cursor.execute('SELECT class FROM tbl_class')
            result = cursor.fetchall()
            for cs in range(len(result)):
                if tmp == result[cs][0]:
                    tmp2 = words[num]
                    for wo in range(num+1,len(words)):
                        tmp2 = tmp2 + words[wo]
                    return Class(tmp,tmp2)
            tmp = words[0]+words[1]+words[2]+words[3]
            nmu=4
            cursor = connection.cursor()
            cursor.execute('SELECT class FROM tbl_class')
            result = cursor.fetchall()
            for cs in range(len(result)):
                if tmp == result[cs][0]:
                    tmp2 = words[num]
                    return Class(tmp,tmp2)
            tmp = words[0]+words[1]+words[2]+words[3]+words[4]
            return Class(tmp)

        elif len(words) == 6:
            tmp = words[0]
            cursor = connection.cursor()
            cursor.execute('SELECT class FROM tbl_class')
            result = cursor.fetchall()
            for cs in range(len(result)):
                if tmp == result[cs][0]:
                    tmp2 = words[1]
                    for wo in range(2,len(words)):
                        tmp2 = tmp2 + words[wo]
                    return Class(tmp,tmp2)
            tmp = words[0]+words[1]
            num=2
            cursor = connection.cursor()
            cursor.execute('SELECT class FROM tbl_class')
            result = cursor.fetchall()
            for cs in range(len(result)):
                if tmp == result[cs][0]:
                    tmp2 = words[num]
                    for wo in range(num+1,len(words)):
                        tmp2 = tmp2 + words[wo]
                    return Class(tmp,tmp2)
            tmp = words[0]+words[1]+words[2]
            num=3
            cursor = connection.cursor()
            cursor.execute('SELECT class FROM tbl_class')
            result = cursor.fetchall()
            for cs in range(len(result)):
                if tmp == result[cs][0]:
                    tmp2 = words[num]
                    for wo in range(num+1,len(words)):
                        tmp2 = tmp2 + words[wo]
                    return Class(tmp,tmp2)
            tmp = words[0]+words[1]+words[2]+words[3]
            nmu=4
            cursor = connection.cursor()
            cursor.execute('SELECT class FROM tbl_class')
            result = cursor.fetchall()
            for cs in range(len(result)):
                if tmp == result[cs][0]:
                    tmp2 = words[num]
                    for wo in range(num+1,len(words)):
                        tmp2 = tmp2 + words[wo]
                    return Class(tmp,tmp2)
            tmp = words[0]+words[1]+words[2]+words[3]+words[4]
            nmu=5
            cursor = connection.cursor()
            cursor.execute('SELECT class FROM tbl_class')
            result = cursor.fetchall()
            for cs in range(len(result)):
                if tmp == result[cs][0]:
                    tmp2 = words[num]
                    return Class(tmp,tmp2)
            tmp = words[0]+words[1]+words[2]+words[3]+words[4]+words[5]
            return Class(tmp)

        return Class(Check_Class(tmp,words,num))

def teacher(teacher_name,content=random):
    # connection = MySQLdb.connect(host, user, passwd,.etc)    cursor = connection.cursor()
    cursor.execute('SELECT*FROM tbl_teacher')
    columns=['性格','特徴','担当授業','総合評価','裏情報','裏情報２']
    musubi=['です。','だよ。','の授業を担当しています。','だよ。','らしいよ。','らしいよ']
    result = cursor.fetchall()

    if teacher_name.endswith("先生",len(teacher_name)-2,len(teacher_name)-1)==False:
        teacher_name=teacher_name+("先生")
    if content==random:
        id=random.randint(2,len(columns)+1)
    else:
        if content in columns:
            id=columns.index(content)+2
        else:
            return (teacher_name+"の"+content+"は登録されていないよ")
    for row in result:
        if row[1]==teacher_name:
            if id==5:
                return(teacher_name+'の評価は'+"☆"*int(row[id])+musubi[id-2])
            else:
                return (teacher_name+'は'+row[id]+musubi[id-2])
    return (teacher_name+"は今学校にはいないよ")



def Class(class_name,content=random):
    # connection = MySQLdb.connect(host, user, passwd,.etc)
    cursor = connection.cursor()
    cursor.execute('SELECT*FROM tbl_class')
    columns=['単位期待度','成績評価方法','ためになる度']
    result = cursor.fetchall()
    if content==random:
        id=random.randint(2,len(columns)+1)
    else:
        if content=="単位":
            content = "単位期待度"
        if content=="ため度" or content=="ため":
            content = "ためになる度"
        if content=="成績評価":
            content = "成績評価方法"
        if content in columns:
            id=columns.index(content)+2
        else:
            return (class_name+"の"+content+"は登録されていないよ")
    for row in result:
        if row[1]==class_name:
            return (class_name+"の"+columns[id-2]+"は"+row[id]+"だよ。")
    return class_name+"は登録されていないよ"

