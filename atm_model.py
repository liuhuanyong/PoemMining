#!/usr/bin/env python3
# coding: utf-8
# File: atm_model.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-8-6
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim.models import AuthorTopicModel
from gensim import corpora
from sklearn.manifold import TSNE
import pymongo
import matplotlib.pyplot as plt


class AuthorMining:
    def __init__(self):
        conn = pymongo.MongoClient()
        self.db = conn['shici']['data']


    '''构造训练语料'''
    def build_corpus(self):
        f = open('corpus_train.txt', 'w+')
        count = 0
        for item in self.db.find():
            count += 1
            print(count)
            author = item['author']
            content = [i.split('/')[0] for i in item['seg_content'] if i.split('/')[-1] not in ['w']]
            f.write(author + '\t' + ' '.join(content) + '\n')
        f.close()

    '''进行atm模型'''
    def atm_model(self):
        docs = []
        author2doc = {}
        index = 0
        for line in open('corpus_train.txt'):
            line = line.strip()
            if not line:
                continue
            author = line.split('\t')[0]
            if author not in author2doc:
                author2doc[author] = [index]
            else:
                author2doc[author].append(index)
            doc = line.split('\t')[1].split(' ')
            docs.append(doc)
            index += 1
        print(len(docs))
        # 构建词典
        dictionary = corpora.Dictionary(docs)
        # 对文本进行向量化
        corpus = [dictionary.doc2bow(doc) for doc in docs]
        # 使用atm模型进行训练
        model = AuthorTopicModel(corpus, author2doc = author2doc, id2word = dictionary, num_topics = 100)
        # 保存模型
        model.save('author_topic.model')


    '''加载训练好的authormodel进行测试'''
    def test_model(self):
        model = AuthorTopicModel.load('author_topic.model')
        # 每个作者的向量，每个作者向量维度不一样，对应的主题不一样，主题分别是概率。
        author_vecs = [model.get_author_topics(author) for author in model.id2author.values()]
        print(len(author_vecs))
        for author in author_vecs:
            print(author, len(author))
        # 介绍每位作者
        authors = model.id2author.values()
        print(len(authors), authors)
        # 显示某位作者的向量
        print(model['李白'])
        # 显示模型主题
        for topic in model.show_topics(num_topics=100):
            print(topic)

    '''对作者进行聚类分析'''
    def author_cluster(self):
        model = AuthorTopicModel.load('author_topic.model')
        tsne = TSNE(n_components=2, random_state=0)
        smallest_author = 0
        authors = [model.author2id[a] for a in model.author2id.keys() if len(model.author2doc[a]) >= smallest_author]
        embeddings = tsne.fit_transform(model.state.gamma[authors, :])
        authors = list(model.id2author.values())

        labels = ['柳永','晏殊','欧阳修','李煜','李清照','范仲淹','苏轼','辛弃疾','岳飞']
        author_ids = [model.author2id[author] for author in labels]
        author_embs = tsne.fit_transform([embeddings[i] for i in author_ids])
        print(authors, author_ids, author_embs)
        self.plot_with_labels(author_embs, labels)

        #
        # plot_only = 150
        # low_dim_embs = tsne.fit_transform(embeddings[:plot_only, :])
        # labels = [authors[i] for i in range(plot_only)]
        # self.plot_with_labels(low_dim_embs, labels)




    '''对二维embedding进行展示'''
    def plot_with_labels(self, low_dim_embs, labels, filename='authors.png'):
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.figure(figsize=(18, 18))  # in inches
        for i, label in enumerate(labels):
            print(labels)
            x, y = low_dim_embs[i, :]
            plt.scatter(x, y)
            plt.annotate(label,
                         xy=(x, y),
                         xytext=(5, 2),
                         textcoords='offset points',
                         ha='right',
                         va='bottom')

        plt.savefig(filename)

handler = AuthorMining()
handler.author_cluster()