# -*- coding:utf-8 -*-
import requests
import re
from lxml import etree

def download_page(url):
    """获取url地址页面内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get(url).content
    # print data
    he = etree.HTML(data)
    url = he.xpath('//li/div/div/div/a/@href')
    name = he.xpath('//li/div/div/div/a/span[1][@class="title"]/text()')


    # print url
    # print name[0]
    # print type(name)
    i = 1 
    for x in name:
    	print str(i) + '. ' + x
    	i = i+1

if __name__ == "__main__":
    url = 'http://movie.douban.com/top250/'
    download_page(url)