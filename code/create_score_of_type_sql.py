#将词性评分写入sql中
#放入提交的代码中
import re
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

label_list=['a','b','c','d','e','f','g','h','i','m','n','o','p','q','r','s','u','v']

def write_to_sql():
    con=conn()
    cursor=con.cursor()
    num=0
    for i in label_list:
        for j in label_list:
            num+=1
            insertmsg1 = """INSERT INTO seg_standard(seq1,seq2,score) values """
            insertmsg1 += "(" + "'" + i + "','"+j+"',"
            if i==j:
                insertmsg1+="0)"
            else:
                insertmsg1+="-2)"
            print(num)
            #print(insertmsg1)
            cursor.execute(insertmsg1)
            con.commit()

write_to_sql()