# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 16:30:13 2017

@author: ejimahideaki
"""

import MySQLdb
import random
def teacher(teacher_name):
    connection = MySQLdb.connect(host='52.196.141.5', user='ec2user', passwd='yourpassword', db='intern0821', charset='utf8')
    cursor = connection.cursor()
    cursor.execute('SELECT*FROM tbl_teacher')
    columns=['性格','特徴','担当授業','総合評価','裏情報','裏情報２']
    musubi=['です。','だよ。','の授業を担当しています。','だよ。','らしいよ。','らしいよ']
    result = cursor.fetchall()
    
    for row in result:
        id=random.randint(2,len(row)-1)
        if row[1]==teacher_name:
            if id==5:
                return(teacher_name+'の評価は'+"☆"*int(row[id])+musubi[id-2])
            else:
                return (teacher_name+'は'+row[id]+musubi[id-2])
            return (teacher_name+"は今学校にはいないよ")

def Class(class_name):
    connection = MySQLdb.connect(host='52.196.141.5', user='ec2user', passwd='yourpassword', db='intern0821', charset='utf8')
    cursor = connection.cursor()
    cursor.execute('SELECT*FROM tbl_class')
    columns=['単位期待度','成績評価方法','ためになる度']
    result = cursor.fetchall()
    for row in result:
        id=random.randint(2,len(row)-1)
        if row[1]==class_name:
            return (class_name+"の"+columns[id-2]+"は"+row[id]+"だよ。")
    return class_name+"は登録されていないよ"
print(teacher("加藤先生"))
print(Class("微分積分"))