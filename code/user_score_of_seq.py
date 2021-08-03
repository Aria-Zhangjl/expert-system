#根据规则计算出用户的对联评分
#放入提交的代码中
import user_score_of_tone
import user_score_of_structure
import user_score_of_similarity
import pyodbc
import random

sum=478967

DRIVER='{SQL Server}'
server=r'LAPTOP-2CLBJL3I'
user=r'sa'
psd=r'st_zjl20000116'
db=r'regulation'

tone_dict={'ping':'平','ze':'仄','tong':'通'}

rule=[]

def conn():
    connect = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-2CLBJL3I;DATABASE=regulation;UID=sa;PWD=st_zjl20000116') #服务器名,账户,密码,数据库名
    if connect:
        print("连接成功!")
    else:
        print('连接失败！')
    return connect


#检测是否输入的都是汉字
def is_chinese(string):
    for ch in string:
        if '\u4e00' <= ch <= '\u9fff':
            continue
        else:
            return False
    return True

#随机给出一个上联
def random_seq1():
    test_id = random.randint(0, sum)
    con = conn()
    cursor = con.cursor()
    sql = """select seq1 from seq_data where id = """ + str(test_id)
    cursor.execute(sql)
    test = cursor.fetchone()
    con.commit()
    test = test[0]
    return test

#判断输入是否合理
def process_input(test,user_input):
    rule[0]=[]
    if(len(test) != len(user_input)):
        rule[0].append("字数不匹配")
    elif is_chinese(user_input) == False:
        rule[0].append("包含错误的字符")
    # 开始进入推理
    else:
        score1,rule[1]=score_of_tone(test,user_input)  #平仄
        score2,rule[2]=score_of_structure(test,user_input) #词性结构
        score3,rule[3]=score_of_similarity(test,user_input) #上下联相似性
        print(score1,score2,score3)
        print("总评分为："+str(40+score1+score2+score3))

#判断基础得分
def basic_score(seq1,seq2):
    score=0
    if (len(seq1) != len(seq2)):
        rule.append("字数不匹配")
    elif is_chinese(seq2) == False:
        rule.append("包含错误的字符")
    else:
        score=40
        rule.append("字数统一，输入格式正确")
    return score,rule


# 获取上下联的平仄的评分和选取的知识
def score_of_tone(seq1,seq2):
    #seq1="月光千里白"
    #seq2="秋色一天青"
    #得到汉字列表
    tone1,tone_rule1=user_score_of_tone.get_tone(seq1)
    tone2,tone_rule2=user_score_of_tone.get_tone(seq2)
    #开始逐字分析
    score,obey_rule=user_score_of_tone.check_tone(tone1, tone2)
    rules=tone_rule1+tone_rule2+obey_rule
    return 20+score,rules

#计算词性结构的评分
def score_of_structure(seq1,seq2):
    score,obey_rule1,obey_rule2=user_score_of_structure.seek_from_sql([seq1, seq2])
    rules=obey_rule1+obey_rule2
    return 20+score,rules

def score_of_similarity(seq1,seq2):
    obey_rule="两幅对联的相似性为："
    score=user_score_of_similarity.process_input(seq1, seq2)
    obey_rule+=str(score)
    score=score*20
    return score,obey_rule


#检测是否有生僻字
#def score_of_hanzi_freq(seq1,seq2):
    #process_input()

#process_input()