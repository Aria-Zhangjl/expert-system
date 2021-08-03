#把收集到的上联写入sql中，最后的成果是随机选择
#放入提交的sql代码
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

def read_seq():
    all_seq=[]
    with open("in.txt","r",encoding='utf-8') as f:
        data1=f.readlines()
    for each in data1:
        each=each.replace(" ","")
        each=each.replace("\n","")
        if(len(each)<=7):
            all_seq.append(each)

    with open("in1.txt","r",encoding='utf-8') as f:
        data1=f.readlines()
    for each in data1:
        each = each.replace(" ", "")
        each = each.replace("\n", "")
        if (len(each) <= 7):
            all_seq.append(each)
    return all_seq


#把上联写入sql中
def write_into_sql():
    all_seq=read_seq()
    i=0
    con=conn()
    cursor=con.cursor()
    for each in all_seq:
        i+=1
        insertmsg1 = """INSERT INTO seq_data(id,seq1) values """
        insertmsg1+="("+str(i)+",'"+each+"')"
        print(insertmsg1)
        cursor.execute(insertmsg1)
        con.commit()

write_into_sql()