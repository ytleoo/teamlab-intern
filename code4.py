# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 11:43:49 2017

@author: ejimahideaki
"""


import MySQLdb
import random
def teacher(teacher_name,content=random):
    connection = MySQLdb.connect(host='52.196.141.5', user='ec2user', passwd='yourpassword', db='intern0821', charset='utf8')
    cursor = connection.cursor()
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
    connection = MySQLdb.connect(host='52.196.141.5', user='ec2user', passwd='yourpassword', db='intern0821', charset='utf8')
    cursor = connection.cursor()
    cursor.execute('SELECT*FROM tbl_class')
    columns=['単位期待度','成績評価方法','ためになる度']
    result = cursor.fetchall()
    if content==random:
        id=random.randint(2,len(columns)+1)
    else:
        if content in columns:
            id=columns.index(content)+2
        else:
            return (class_name+"の"+content+"は登録されていないよ")
    for row in result:
        if row[1]==class_name:
            return (class_name+"の"+columns[id-2]+"は"+row[id]+"だよ。")
    return class_name+"は登録されていないよ"
    
        
print(teacher("加藤",))
#print(Class("微分積分","ためになる度"))
#print(Class("微分","ためになる度"))