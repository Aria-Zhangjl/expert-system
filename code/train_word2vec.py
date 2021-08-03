#根据语料库训练单词
# 训练word2vec
# 放入提交的代码中
import warnings

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.models import word2vec
import logging

# 主程序
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = word2vec.Text8Corpus(u"seg_data.txt")  # 加载语料
n_dim = 300
# 训练skip-gram模型;
model = word2vec.Word2Vec(sentences, vector_size=n_dim, min_count=0, sg=1)
model.save("word2vec.model")

'''
# 计算两个词的相似度/相关程度
y1 = model.wv.similarity(u"鱼女", u"雷公")
print(y1)
print("--------")
'''
