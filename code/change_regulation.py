#修改规则
#放入提交的代码中
import pyodbc
import os
import sys


DRIVER='{SQL Server}'
server=r'LAPTOP-2CLBJL3I'
user=r'sa'
psd=r'st_zjl20000116'
db=r'regulation'

label_list=['a','b','c','d','e','f','g','h','i','m','n','o','p','q','r','s','n','u','v']

def conn():
    connect = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-2CLBJL3I;DATABASE=regulation;UID=sa;PWD=st_zjl20000116') #服务器名,账户,密码,数据库名
    if connect:
        print("连接成功!")
    else:
        print('连接失败！')
    return connect

#修改汉字的平仄
def change_tone_of_hanzi(ch,tone1):
    '''

    :param ch: 要修改的汉字
    :param tone1: 拼音
    :return:
    '''
    con=conn()
    cursor=con.cursor()
    mess="update tone_table set tone = '"+tone1+"' where hanzi = "+"N'"+ch+"'"
    #print(mess)
    cursor.execute(mess)
    con.commit()

#删除汉字的平仄规则
def delete_hanzi_tone(ch):
    '''

    :param ch:
    :return:
    '''
    con=conn()
    cursor=con.cursor()
    mess="delete from tone_table where hanzi = N'"+ch+"'"
    cursor.execute(mess)
    con.commit()

#添加汉字的平仄规则
def add_hanzi_tone(ch,tone):
    '''

    :param ch:
    :return:
    '''
    con=conn()
    cursor=con.cursor()
    mess="""INSERT INTO tone_table(hanzi,tone) values """
    mess+="(N'"+ch+"','"+tone+"')"
    cursor.execute(mess)
    con.commit()

#修改平仄的评分
def change_score_of_tone(s,seq1,seq2):
    con=conn()
    cursor=con.cursor()
    mess="update tone_regulation set score = "+str(s)+" where seq1 = '"+seq1+"' and seq2 = '"+seq2+"'"
    cursor.execute(mess)
    con.commit()


#对表格seg_table

#修改词性
def change_label_of_word(type,label):
    con=conn()
    cursor=con.cursor()
    #先检查是否有该label存在
    mess = """update seg_table set label = '"""+label+"' where type = '"+type+"'"
    cursor.execute(mess)
    con.commit()
#对表格seg_standard
#修改评分
def chang_label_score(s,seq1,seq2):
    con=conn()
    cursor=con.cursor()
    mess="""update seg_standard set score ="""+str(s)+"""where seq1 ='"""+seq1+"""' and seq2='"""+seq2+"""'"""
    cursor.execute(mess)
    con.commit()
