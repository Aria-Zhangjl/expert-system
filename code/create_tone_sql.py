#在sqlserver建立关于音调的规则库
#放入提交的代码中
#coding=utf8
import re
import pyodbc
import os
import sys


DRIVER='{SQL Server}'
server=r'LAPTOP-2CLBJL3I'
user=r'sa'
psd=r'st_zjl20000116'
db=r'regulation'

def conn():
    connect = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-2CLBJL3I;DATABASE=regulation;UID=sa;PWD=st_zjl20000116') #服务器名,账户,密码,数据库名
    if connect:
        print("连接成功!")
    else:
        print('连接失败！')
    return connect

#建立平仄通的对应表
ping=[]
ze=[]
tong=[]
def load_rhythm_list():
    """
    载入平水韵表并转换为dict形式
    """
    with open("平水韵表.txt", encoding="UTF-8") as file:
        rhythm_lines = file.readlines()
    rhythm_dict = dict()
    for rhythm_line in rhythm_lines:
        rhythm_name = re.search(".*(?=[平上去入]声:)", rhythm_line).group()  # 读取韵部名称
        rhythm_tune = re.search("[平上去入](?=声:)", rhythm_line).group()  # 读取韵部声调
        rhythm_characters = re.sub(".*[平上去入]声:", "", rhythm_line)  # 获取韵部包含的所有文字
        for character in rhythm_characters:
            if character not in rhythm_dict:
                rhythm_dict[character] = list()
            rhythm_dict[character].append([rhythm_name, rhythm_tune])
    return rhythm_dict


RHYTHM_LIST = load_rhythm_list()  # 导入平水韵表


def form_tone_table():
    for hanzi in RHYTHM_LIST:
        if(len(RHYTHM_LIST[hanzi])>1):
            tong.append(hanzi)
        else:
            if RHYTHM_LIST[hanzi][0][1]=="平":
                ping.append(hanzi)
            else:
                ze.append(hanzi)
    return ping,ze,tong

def writ_table_into_sql(ping,ze,tong):
    con = conn()
    cursor = con.cursor()
    #insertmsg0="""if NOT exists(SELECT * FROM tone_table WHERE hanzi="""
    insertmsg1 = """INSERT INTO tone_table(hanzi,tone) values """
    #insertmsg2 = ""
    for ch in ping:
        insertmsg0 = """if NOT exists(SELECT * FROM tone_table WHERE hanzi="""
        insertmsg0+="N'"+ch+"')"
        insertmsg2="(N'"+ch+"','平'"+")"
        insertmsg=insertmsg0+insertmsg1+insertmsg2
        #print(insertmsg)
        cursor.execute(insertmsg)
        con.commit()
        #print("sus")
    insertmsg2 = ""
    for ch in ze:
        insertmsg0 = """if NOT exists(SELECT * FROM tone_table WHERE hanzi="""
        insertmsg0+="N'"+ch+"')"
        insertmsg2="(N'"+ch+"','仄'"+")"
        insertmsg=insertmsg0+insertmsg1+insertmsg2
        #print(insertmsg)
        cursor.execute(insertmsg)
        con.commit()
    insertmsg2 = ""
    for ch in tong:
        insertmsg0 = """if NOT exists(SELECT * FROM tone_table WHERE hanzi="""
        insertmsg0+="N'"+ch+"')"
        insertmsg2="(N'"+ch+"','通'"+")"
        insertmsg=insertmsg0+insertmsg1+insertmsg2
        #print(insertmsg)
        cursor.execute(insertmsg)
        con.commit()


ping,ze,tong=form_tone_table()

writ_table_into_sql(ping,ze,tong)






