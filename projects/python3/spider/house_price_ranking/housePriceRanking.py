# -*- coding:utf-8 -*-
import requests
from lxml import etree
import collections


urls = ['http://esf.taizhou.fang.com/house-xm1818080456/i3{}/'.format(str(i)) for i in range(2,25,1)]
print(urls)

#there is some issues in gotWeb, will return some unknown websites.. using urls behind instead
def gotWeb(url):
    baseUrl = 'http://esf.taizhou.fang.com/'
    wbData = requests.get(url).content.decode("gbk")
    tree = etree.HTML(wbData)
    websites = tree.xpath('//*[@id="list_D10_15"]/a/@href')
    webs = []
    for web in websites:
        webs.append(baseUrl+web)
    return(webs)

data = []
# info = collections.OrderedDict()
def gotData(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    wbData = requests.get(url,headers=headers).content.decode("gbk")
    tree = etree.HTML(wbData)
    prices = tree.xpath('//*[@class="info rel floatr"]/div[3]/p[1]/span[1]/text()')
    areas  = tree.xpath('//*[@class="info rel floatr"]/div[2]/p[1]/text()')
    averages = tree.xpath('//*[@class="info rel floatr"]/div[@class="moreInfo"]/p[2]/text()[1]')
    print(areas)
    print(prices)
    print(averages)
    for area,price,average in zip(areas,prices,averages):
        info = {
            'area':area,
            'price':price,
            'average':average
        }
        #seem ordereddict will store all the same walue as the last value
        # info['area'] = area
        # info['price'] = price
        # info['average'] = average
        data.append(info)

url = 'http://esf.taizhou.fang.com/house-xm1818080456/'
gotData(url)
count = 2
for i in urls:
    gotData(i)
    print(count)
    count = count + 1

print(len(data))
print(data)





