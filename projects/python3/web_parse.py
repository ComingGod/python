from bs4 import BeautifulSoup
import requests
from lxml import etree
import time
import json
import yaml

url = 'https://cn.tripadvisor.com/Attractions-g60763-Activities-New_York_City_New_York.html'
urls = ['https://cn.tripadvisor.com/Attractions-g60763-Activities-c47-oa{}-New_York_City_New_York.html#FILTERED_LIST'.format(str(i)) for i in range(30,100,30)]

data = []
def get_data(url):
    wb_data = requests.get(url).content
    soup = BeautifulSoup(wb_data, 'lxml')
    titles  = soup.select('div.listing_title > a[target="_blank"]')
    images  = soup.select('img[width="180"]')
    cates   = soup.select('div.p13n_reasoning_v2')
    for title,image,cate in zip(titles,images,cates):
        info = {
            'title': title.get_text(),
            'image': image.get('src'),
            'cate' : list(cate.stripped_strings),
        }
        print (info)
        data.append(info)

for url in urls:
    get_data(url)
    time.sleep(2)
    print('*'*20)
# for item in data:
#     item['title'].encode('utf8')
#     for i in item['cate']:
#         i.encode('utf8')


with open('result.txt','w+') as fp:
    for item in data:
        # yaml.dump(item,fp)
        fp.write('%s\t%s\t%s\n' %(item['cate'],item['title'],item['image']))



# tag = soup.find_all('div')
# print(soup.div)
# print(soup.name)
# print(soup.div.name)
# print(soup.div.attrs)
# print(soup.body.contents)

# images = soup.find_all(width="180")
# print(images[0].attrs)
#
# print(soup.select('div .listing_title > a'))

# Xpath methon
# //*[@id="ATTR_ENTRY_"]/div[2]/div/div/div[1]/div[2]/a
# //*[@id="lazyload_617225327_23"]
# //*[@id="ATTR_ENTRY_"]/div[2]/div/div/div[2]/a

# ha = etree.HTML(wb_data)
# titles = ha.xpath('//*[@id="ATTR_ENTRY_"]/div[2]/div/div/div[1]/div[2]/a/text()')
# images = ha.xpath('//*[@id="ATTR_ENTRY_"]/div[2]/div/div/div[2]/a/img[@width="180"]/@src')
#
# data = []
# for title,image in zip(titles,images):
#     info = {
#         'title' : title,
#         'image' : image,
#     }
#     print(info)
#     data.append(info)
# # print (data[0])






