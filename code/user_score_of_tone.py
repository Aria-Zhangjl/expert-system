#检验对联的平仄，返回得分
#放入提交代码中
import pyodbc

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

"""
对输入的诗句逐字进行平仄分析
"""

def get_tone(hanzi_list):
    obey_rule=[]
    tone_list=[]
    con = conn()
    cursor = con.cursor()
    pronj="==>"
    for subsentence in hanzi_list:
        tone_res=""
        for character in subsentence:
            insertmsg1 = """select tone from tone_table where hanzi =  '""" + character + """'"""
            cursor.execute(insertmsg1)
            tone = cursor.fetchone()
            if tone == None:
                tone=['通']
            tone_res += tone[0]
            con.commit()
            obey_rule.append(character+pronj+tone[0])
        tone_list.append(tone[0])
    #print(tone_list)
    return tone_list,obey_rule


"""
对输入的诗句逐字判断其平仄是否匹配
把规则写入数据库中
"""
def check_tone(tone1,tone2):
    obey_rule=[]
    minus=0
    pronj="相对"
    con=conn()
    cursor=con.cursor()
    #根据数据库中的评分规则进行推理
    for i in range(len(tone1)):
        mess = """select score from tone_regulation where seq1 like '"""
        mess+= tone1[i]
        mess += """' and seq2 like '"""
        mess +=tone2[i]+"'"
        #print(mess)
        cursor.execute(mess)
        score=cursor.fetchone()
        con.commit()
        #print(score)
        if score[0] !=0:
            obey_rule.append("第"+str(i+1)+"个字分别是："+tone1[i]+"和"+tone2[i]+"不相对,"+str(score[0]))
        minus+=score[0]
    return minus,obey_rule








if __name__ == "__main__":
    str1=input("上联：")
    str2=input("下联：")
    tone1=[]
    tone2=[]
    str1=str1.split("，")
    str2=str2.split("，")
    tone1=get_tone(str1)
    tone2=get_tone(str2)
    #print(tone1)
    #print(tone2)