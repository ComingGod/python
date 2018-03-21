# -*- coding:utf-8 -*-
import requests
import re
from lxml import etree
import os

def PageInfo(data):
    he = etree.HTML(data)
    url = he.xpath('//li/div/div/div/a/@href')
    name = he.xpath('//li/div/div/div/a/span[1][@class="title"]/text()')
    ratingNum = he.xpath('//li/div/div/div/div/span[2]/text()')
    assert(len(name) == len(url))
    # return ([i for i in (name,url,ratingNum)])
    # return zip(name,url),ratingNum
    return [name, url, ratingNum]

def Spider(url):
    data = requests.get(url).content
    nextPage = re.findall(r'<a href="(.*?);filter=" >.*?</a>',data)
    for i in range(len(nextPage)):
        nextPage[i] = url + nextPage[i]
    # print nextPage
    gotData = PageInfo(data)
    for i in nextPage:
        data = requests.get(i).content
        gotData2 = PageInfo(data)
        for j in range(len(gotData)):
        	gotData[j].extend(gotData2[j])

    print '*'*20
    print gotData
    print os.getcwd()
    fp = open('movieRanking.txt','w+')
    for i in range(len(gotData[0])):
    	fp.write('%s\t\t%s\t%s\n' %(gotData[0][i].encode('utf8'), gotData[1][i].encode('utf8'), gotData[2][i].encode('utf8')))

if __name__ == "__main__":
    url = 'http://movie.douban.com/top250/'
    Spider(url)