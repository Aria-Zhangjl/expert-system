#对全唐诗和对联进行hanlp分词
#放入提交的代码中
from pyhanlp import *
import re
import thulac

with open("data.txt","r",encoding='utf-8') as f:
    data=f.readlines()

seg_data=[]
for i in range(len(data)):
    if(data[i]=='\n'):
        continue
    seg=HanLP.segment(data[i])
    string=""
    for j in range(len(seg)):
        seg[j]=str(seg[j])
        seg[j]=re.search("^[^/]*", seg[j]).group()
        string+=seg[j]+" "
    string+='\n'
    seg_data.append(string)

with open("seg_data.txt","w",encoding='utf-8') as f:
    for i in range(len(seg_data)):
        f.write(seg_data[i])




