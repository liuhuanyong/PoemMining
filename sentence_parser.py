#!/usr/bin/env python3
# coding: utf-8
# File: sentence_parser.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-3-10
import os
import re
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer

class LtpParser():
    def __init__(self):
        LTP_DIR = "./ltp_data"
        self.segmentor = Segmentor()
        self.segmentor.load(os.path.join(LTP_DIR, "cws.model"))

        self.postagger = Postagger()
        self.postagger.load(os.path.join(LTP_DIR, "pos.model"))

        self.parser = Parser()
        self.parser.load(os.path.join(LTP_DIR, "parser.model"))

        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(os.path.join(LTP_DIR, "ner.model"))

    '''长句切分'''
    def seg_long_sents(self, content):
        return [sentence for sentence in re.split(r'[？?！!。\n\r]', content.replace(' ','').replace('\u3000','').replace('——','')) if sentence]

    '''ltp基本操作'''
    def basic_parser(self, words):
        postags = list(self.postagger.postag(words))
        netags = self.recognizer.recognize(words, postags)
        return postags, netags

    '''基于实体识别结果,整理输出实体列表'''
    def format_entity(self, words, netags):
        name_entity_list = []
        place_entity_list = []
        organization_entity_list = []
        ntag_E_Nh = ""
        ntag_E_Ni = ""
        ntag_E_Ns = ""
        index = 0
        for item in zip(words, netags):
            word = item[0]
            ntag = item[1]
            if ntag[0] != "O":
                if ntag[0] == "S":
                    if ntag[-2:] == "Nh":
                        name_entity_list.append(word)
                    elif ntag[-2:] == "Ni":
                        organization_entity_list.append(word)
                    else:
                        place_entity_list.append(word)
                elif ntag[0] == "B":
                    if ntag[-2:] == "Nh":
                        ntag_E_Nh = ntag_E_Nh + word
                    elif ntag[-2:] == "Ni":
                        ntag_E_Ni = ntag_E_Ni + word
                    else:
                        ntag_E_Ns = ntag_E_Ns + word
                elif ntag[0] == "I":
                    if ntag[-2:] == "Nh":
                        ntag_E_Nh = ntag_E_Nh + word
                    elif ntag[-2:] == "Ni":
                        ntag_E_Ni = ntag_E_Ni + word
                    else:
                        ntag_E_Ns = ntag_E_Ns + word
                else:
                    if ntag[-2:] == "Nh":
                        ntag_E_Nh = ntag_E_Nh + word
                        name_entity_list.append(ntag_E_Nh)
                        ntag_E_Nh = ""
                    elif ntag[-2:] == "Ni":
                        ntag_E_Ni = ntag_E_Ni + word
                        organization_entity_list.append(ntag_E_Ni)
                        ntag_E_Ni = ""
                    else:
                        ntag_E_Ns = ntag_E_Ns + word
                        place_entity_list.append(ntag_E_Ns)
                        ntag_E_Ns = ""
            index += 1
        return place_entity_list

    '''获取地点'''
    def collect_locations(self, content):
        locations = []
        sents = self.seg_long_sents(content)
        for i in sents:
            words = list(self.segmentor.segment(i))
            postags, netags = self.basic_parser(words)
            locations += self.format_entity(words, netags)

        return locations
