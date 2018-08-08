#!/usr/bin/env python3
# coding: utf-8
# File: poem_process.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-8-6
import jieba.posseg as pseg
import pymongo
import re
from collections import Counter

class PoemMining:
    def __init__(self):
        conn = pymongo.MongoClient()
        self.db = conn['shici']['data']

    '''使用jieba进行分词'''
    def seg_poems_jieba(self, content):
        word_list = [w.word for w in pseg.cut(content) if w.flag[0] not in ['x','w']]
        return word_list

    '''去除括号内的注释'''
    def remove_noisy(self, content):
        pattern = re.compile('\([^(]*\)')
        return pattern.sub('', content)

    '''诗词切分主函数, 处理后存入mongodb数据库'''
    def poems_main(self):
        count = 0
        for item in self.db.find():
            content = item['content']
            seg_content_jieba = self.seg_poems_jieba(content)
            self.db.update({'_id':item['_id']},{'$set':{'seg_content_jieba':seg_content_jieba}})
            count += 1
            print(count)

    '''获取地点类命名实体'''
    def collect_locations(self):
        f = open('top_nss.txt', 'w+')
        nss = []
        count = 0
        for item in self.db.find():
            count += 1
            seg_content = item['seg_content']
            ns = [i.split('/')[0] for i in seg_content if i.split('/')[-1] == 'ns' and len(i.split('/')[0].replace('。','')) > 1]
            if not ns:
                continue
            nss += ns
            print(count)

        ns_dict = {i[0]:i[1] for i in Counter(nss).most_common()}
        for ns, count in ns_dict.items():
            f.write(ns + '\t' + str(count) + '\n')
        f.close()

    '''获取最多star的诗歌或者诗人'''
    def get_most_popular(self):
        f_author = open('top_authors.txt', 'w+')
        f_poems = open('top_poems.txt', 'w+')
        author_dict = {}
        poem_dict = {}
        for item in self.db.find():
            author_star = item["author_stars"]
            poem_star = item['star']
            poem = item['author'] + '@' + item["title"]
            author = item['author'] + '@' + item["dynasty"]
            author_dict[author] = author_star
            poem_dict[poem] = poem_star

        author_dict = sorted(author_dict.items(), key=lambda asd:asd[1], reverse=True)
        poem_dict = sorted(poem_dict.items(), key=lambda asd:asd[1], reverse=True)
        for item in author_dict:
            f_author.write(item[0] + '\t' + str(item[1]) + '\n')
        f_author.close()

        for item in poem_dict:
            f_poems.write(item[0] + '\t' + str(item[1]) + '\n')
        f_poems.close()

    '''通过tag对意象进行处理'''
    def collect_tags(self):
        count = 0
        f_tag = open('top_tags.txt', 'w+')
        for item in self.db.find():
            count += 1
            print(count)
            tags = item['tags']
            if not tags:
                continue
            for tag in tags:
                f_tag.write(tag + '@' + item['author'] + '@' + item['title'].replace(' ','') + '\n')
        f_tag.close()

    '''查找出作者出现的地点信息'''
    def collect_author_location(self):
        author_dict = {}
        f = open('author_location.txt', 'w+')
        for item in self.db.find():
            seg_content = item['seg_content']
            ns = [i.split('/')[0] for i in seg_content if i.split('/')[-1] == 'ns' and len(i.split('/')[0]) > 1]
            if not ns:
                continue
            author = item['author']
            dynasty = item['dynasty']
            pair = author + '@' + dynasty
            if author not in author_dict:
                author_dict[pair] = ns
            else:
                author_dict[pair] += ns

        for author, location in author_dict.items():
            f.write(author + ',' + ';'.join(location) + '\n')
        f.close()

    '''查找指定意象的诗歌'''
    def collect_yixiang(self):
        yixiang = ['写人','写剑','写史','写塔','写景','写月',
                    '写柳','写树','写桥','写梅','写水','写江','写灯','写狗古诗18首',
                    '写琴','写画','写竹','写笋','写船','写花','写茶','写草','写莲',
                    '写虎','写雨','写雪','写风','写马','写鬼','写鱼','写鸟','写鼠']

    '''基于atm模型，对作者进行建模'''
handler = PoemMining()
handler.poems_main()
# handler.collect_tags()
# handler.collect_locations()
# handler.collect_author_location()
