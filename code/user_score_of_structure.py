# 使用HANLP划分后，查表对词进行比较
# 在sql中查询最终的得分
# 放入提交代码中
import re
import pyodbc
from pyhanlp import *

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

# 记录下分词和词性
def select_word_flag(data):
    result = []
    for i in range(len(data)):
        seg = HanLP.segment(data[i])
        pre = []
        for j in range(len(seg)):
            seg[j] = str(seg[j])
            p = seg[j].split('/')
            pre.append(p)
        result.append(pre)
    return result


# 对分词进行修正
def check_structure(result):
    '''

    :param result: 分词后的单词和词性
    [[['绿叶', 'n'], ['红花', 'n'], ['遮', 'v'], ['碧水', 'n']], [['繁星', 'n'], ['明月', 'n'], ['戏', 'n'], ['长空', 'n']]]
    :return:返回匹配个数和修正后的分词
    '''
    score = 0
    len0 = len(result[0])
    len1 = len(result[1])

    seq1 = result[0]
    seq2 = result[1]
    '''
    seq的形式：[['渔歌', 'n'], ['随', 'p'], ['浪涌', 'nz']]
    '''
    #print(seq1)
    #print(seq2)
    #print("here\n")

    if (len0 == len1):
        for i in range(len0):
            if (seq1[i][1] == seq2[i][1]):
                score += 1
        return score, seq1, seq2
    # 长度不相等，一直合并到相等
    else:
        corr1 = []
        corr2 = []
        i = 0
        j = 0
        while j < (min(len1, len0)):
            # 词语的个数相同
            #print("here")
            #print(seq1[i])
            #print(seq2[j])
            #print("end")
            if len(seq2[j][0]) == len(seq1[i][0]):
                #print(seq2[j][0], seq1[i][0])
                corr1.append(seq1[i])
                corr2.append(seq2[j])
                i += 1
                j+=1
            else:
                # 上下同时合并到相等
                new_word1 = seq1[i][0]
                new_word2 = seq2[j][0]
                pj = j
                pi = i
                while len(new_word2) != len(new_word1):
                    if (len(new_word2) < len(new_word1)):
                        new_word2 += seq2[pj + 1][0]
                        pj += 1
                    else:
                        new_word1 += seq1[pi + 1][0]
                        pi += 1
                new_word1_flag = seq1[pi][1]
                new_word2_flag = seq2[pj][1]
                # print("new word1",new_word1)
                # print("new word2",new_word2)
                i = pi + 1
                # print("i",i)
                j = pj+1
                #print("pj.j="+str(j))
                # print("j",j)
                if new_word1_flag == new_word2_flag:
                    score += 1
                corr1.append([new_word1, new_word1_flag])
                corr2.append([new_word2, new_word2_flag])
            #print("i="+str(i))
            #print("j="+str(j))
    return score, corr1, corr2



#从sql中查询各大类
def seek_from_sql(data):
    res = select_word_flag(data)
    score, corr1, corr2 = check_structure(res)
    #print(corr1,corr2)
    obey_rule1=[]
    obey_rule2=[]

    con=conn()
    cursor=con.cursor()
    score=0
    for i in range(len(corr1)):
        select_mess="""select label from seg_table where type = """
        select_mess+="'"+corr1[i][1]+"'"
        #print(select_mess)
        cursor.execute(select_mess)
        flag1 = cursor.fetchone()
        #print(flag1)
        obey_rule1.append(corr1[i][0]+"==>"+corr1[i][1])
        obey_rule1.append(corr1[i][1]+"==>"+flag1[0])
        con.commit()

        select_mess = """select label from seg_table where type = """
        select_mess += "'"+corr2[i][1]+"'"
        #print(select_mess)
        cursor.execute(select_mess)
        flag2 = cursor.fetchone()
        obey_rule1.append(corr2[i][0]+"==>"+corr2[i][1])
        obey_rule1.append(corr2[i][1] + "==>" + flag2[0])
        con.commit()

        flag1[0]=flag1[0].replace(" ","")
        flag2[0]=flag2[0].replace(" ","")
        #再从评分表seg_score中匹配到相应的评分
        select_mess="""select score from seg_standard where seq1 like '"""
        select_mess+=flag1[0] +"""' and seq2 like '"""+flag2[0]+"'"
        #print(select_mess)
        cursor.execute(select_mess)
        score1 =cursor.fetchone()
        score+=score1[0]
        if(score1[0] !=0 ):
            obey_rule2.append("第"+str(i+1)+"个词的词性为："+flag1[0]+" "+flag2[0]+","+str(score1[0]))
    return score,obey_rule1,obey_rule2

def test(data):
    res = seek_from_sql(data)
    #print(res)

#data=["笺寄秋思情万缕","文随春色意千分"]
#test(data)
