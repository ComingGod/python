# -*- coding:utf-8 -*-
import requests
from lxml import etree

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}
url = 'http://esf.taizhou.fang.com/house-xm1818080456/'
wbData = requests.get(url,headers=headers).text
# print(wbData)
tree = etree.HTML(wbData)
# urls = tree.xpath('//*[@class="info rel floatr"]/p[1]/a/@href')
# url = []
# url_main = 'http://esf.taizhou.fang.com'
# for i in urls:
#     url.append(url_main + i)


prices = tree.xpath('//*[@class="info rel floatr"]/div[3]/p[1]/span[1]/text()')
areas  = tree.xpath('//*[@class="info rel floatr"]/div[2]/p[1]/text()')
averages = tree.xpath('//*[@class="info rel floatr"]/div[@class="moreInfo"]/p[2]/text()[1]')

print(prices)
print(areas)
print(averages)
print(len(averages))

# //*[@id="list_D03_01"]/dd/div[@class="moreInfo"]/p[2]


# //*[@id="list_D03_01"]/dd/div[3]/p[2]/text()[1]
# //*[@id="list_D03_01"]/dd/div[2]/p[1]
# //*[@id="list_D03_01"]/dd/div[3]/p[2]/text()[1]



# <a href="/chushou/3_300332712.htm" target="_blank" title="中铁溪源104.9平毛坯满2年118万出售">中铁溪源104.9平毛坯满2年118万出售</a>
# //*[@id="list_D03_01"]/dd
# //*[@id="list_D03_01"]/dd/p[1]/a