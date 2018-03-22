# -*- coding:utf-8 -*-
import requests
from lxml import etree

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
        data.append(info)


url = 'http://esf.taizhou.fang.com/house-xm1818080456/i32/'
gotData(url)
for i in gotWeb(url):
    gotData(i)

# print(areas)
# print(prices)
# print(averages)
# print(len(averages))
# print(data)

# //*[@id="list_D03_01"]/dd/div[@class="moreInfo"]/p[2]


# //*[@id="list_D03_01"]/dd/div[3]/p[2]/text()[1]
# //*[@id="list_D03_01"]/dd/div[2]/p[1]
# //*[@id="list_D03_01"]/dd/div[3]/p[2]/text()[1]



# <a href="/chushou/3_300332712.htm" target="_blank" title="中铁溪源104.9平毛坯满2年118万出售">中铁溪源104.9平毛坯满2年118万出售</a>
# //*[@id="list_D03_01"]/dd
# //*[@id="list_D03_01"]/dd/p[1]/a