#!/usr/bin/env python3
# coding: utf-8
# File: test.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-8-12

from urllib import request
from lxml import etree
from urllib import parse
from sentence_parser import *
import json

class PoetWalk:
    def __init__(self):
        self.name_dict = {i.strip().split(',')[0]:i.strip().split(',')[2:] for i in open('city_map.txt') if len(i.strip().split(',')) == 5}
        self.base = '''
              <!DOCTYPE HTML>
               <html>
                   <head>
                       <meta charset="utf-8"><link rel="icon" href="https://static.jianshukeji.com/highcharts/images/favicon.ico">
                       <meta name="viewport" content="width=device-width, initial-scale=1">
                       <script src="https://img.hcharts.cn/jquery/jquery-1.8.3.min.js"></script>
                       <script src="https://img.hcharts.cn/highmaps/highmaps.js"></script>
                       <script src="https://cdnjs.cloudflare.com/ajax/libs/proj4js/2.3.6/proj4.js"></script>
                   </head>
                   <body>
                       <div id="container" style=" height: 1000px"></div>
                       <script src="https://data.jianshukeji.com/geochina/china.js"></script>
                       <script>
                           var data = [
                                   target_datas
                                   ];

                           var map = new Highcharts.Map('container', {
                               title: {
                                   text: 'author'
                               },
                               mapNavigation: {
                                   enabled: true,
                                   buttonOptions: {
                                       verticalAlign: 'bottom'
                                   }
                               },
                               tooltip: {
                                   useHTML: true,
                                   formatter: function() {
                                       return this.point.name;
                                   }
                               },
                               plotOptions: {
                                   series: {
                                       dataLabels: {
                                           enabled: true
                                       },
                                       marker: {
                                           radius: 3
                                       }
                                   }
                               },
                               series: [{
                                   // 空数据列，用于展示底图
                                   mapData: Highcharts.maps['cn/china'],
                                   showInLegend: false
                               },{
                                   type: 'mappoint',
                                   name: 'author',
                                   data: data
                               }]
                           });
                       <!--});-->
                       </script>
                   </body>
               </html>
               '''
    '''请求数据'''
    def get_html(self, url):
        return request.urlopen(url).read().decode('utf-8')

    '''获取诗人生平事迹'''
    def extract_desc(self, word):
        url = "http://baike.baidu.com/item/%s" % parse.quote(word)
        print(url)
        html = self.get_html(url)
        content = [i for i in html.split('<h2 class="title-text">') if word + '</span>人物生平</h2>' in i]
        selector = etree.HTML(content[0])

        # content = html
        # selector = etree.HTML(content)

        res = [i.xpath('string(.)').replace('\n','').replace('\xa0','') for i in selector.xpath('//div[@class="para"]')]
        desc = ''.join([i for i in res if i])
        return desc

    '''基于生平事迹，挖掘诗人关联地点'''
    def collect_locations(self, name):
        content = self.extract_desc(name)
        handler = LtpParser()
        locations = handler.collect_locations(content)
        if not locations:
            return []
        else:
            locations = [self.transfer_location(i) for i in set(locations)]
        locations =[i for i in locations if i]
        print(locations)
        return locations

    '''基于地点，进行古今地点的转换'''
    def transfer_location(self, loc):
        geo_info = self.name_dict.get(loc, 'na')
        if geo_info != 'na':
            return [loc] + geo_info
        else:
            tmp = self.get_abs_geo(loc)
            if not tmp:
                return []
            else:
                return tmp

    '''调用远程api，获取绝对经纬度'''
    def get_abs_geo(self, word):
        url = 'https://apis.map.qq.com/jsapi?qt=poi&wd='+parse.quote(word)
        print(url)
        data = request.urlopen(url).read().decode('gbk')
        data_json = json.loads(data)
        name = ''
        lon = 0
        lat = 0
        if 'pois' in data_json['detail']:
            if len(data_json['detail']['pois']) > 0:
                city_info = data_json['detail']['pois'][0]
                name = word
                lon = str(city_info['pointx'])
                lat = str(city_info['pointy'])
        else:
            if 'city' in data_json['detail']:
                city_info = data_json['detail']['city']
                lon = str(city_info['pointx'])
                lat = str(city_info['pointy'])
                name = city_info['cname']

        if name == '全国':
            return []
        if name and lon and lat:
            return [word, name, lat, lon]
        else:
            return []


    '''挖掘主函数'''
    def mining_main(self, name):
        locations = self.collect_locations(name)
        self.create_html(name, locations)

    '''传入地点数据，绘制足迹地图'''
    def create_html(self, name, locations):
        datas = ''
        for loc in locations:
            if '国' not in loc[1]:
                body = "{name:"+ "'{0}', lat:{1}, lon:{2}".format(loc[1], loc[2], loc[3]) + "},\n"
                datas += body.replace('"','')

        html = self.base.replace('target_datas', datas).replace('author', name + '足迹地图')
        f = open('{0}.html'.format(name), 'w+')
        f.write(html)
        f.close()
        return

name = '李清照'
handler = PoetWalk()
handler.mining_main(name)