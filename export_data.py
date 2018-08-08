#!/usr/bin/env python3
# coding: utf-8
# File: export_data.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-8-8

import pymongo

class LawSpider:
    def __init__(self):
        conn = pymongo.MongoClient()
        self.db = conn['shici']['data']


    '''导出诗词数据'''
    def export_data(self):
        i = 0
        for item in self.db.find():
            i += 1
            print(i)
            title = item['title'].replace('/','').replace(' ','')
            dynasty = item['dynasty']
            author = item['author']
            tags = ';'.join(item['tags'])
            star = str(item['star'])
            author_stars = str(item['author_stars'])
            content = item['content']
            filename = '-'.join([dynasty, author, title])
            f = open('corpus_poem/%s.txt' % filename, 'w+')
            f.write('dynasty:' + dynasty + '\n')
            f.write('author:' + author + '\n')
            f.write('tags:' + tags + '\n')
            f.write('star:' + star + '\n')
            f.write('author_stars:' + author_stars + '\n')
            f.write('title:' + title + '\n')
            f.write('content:' + content + '\n')
            f.close()
        return


handler = LawSpider()
handler.export_data()