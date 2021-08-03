#测试上下联之间的关联性
#放入提交代码
from gensim.models import word2vec
import jieba
from pyhanlp import *
import re
model = word2vec.Word2Vec.load('word2vec.model')

#seq1和seq2是已经分词的词组
def similarity(seq1,seq2):
    score=0
    score1=0
    score2=0
    for i in range(min(len(seq1),len(seq2))):
        score1+=model.wv.similarity(seq1[i],seq2[i])
        #print(score1)
    for j in range(len(seq2)-1):
        score2+=model.wv.similarity(seq2[j],seq2[j+1])
        #print(score2)
    score1/=min(len(seq1),len(seq2))
    score2/=len(seq2)
    score=score1+score2
    return score

def process_input(seq1,seq2):
    seq_list=[]
    seg1 = HanLP.segment(seq1)
    string = []
    for j in range(len(seg1)):
        seg1[j] = str(seg1[j])
        seg1[j] = re.search("^[^/]*", seg1[j]).group()
        string.append(seg1[j])
    seq_list.append(string)
    string=[]
    seg2 = HanLP.segment(seq2)
    for j in range(len(seg2)):
        seg2[j] = str(seg2[j])
        seg2[j] = re.search("^[^/]*", seg2[j]).group()
        string.append(seg2[j])
    seq_list.append(string)
    return similarity(seq_list[0],seq_list[1])

