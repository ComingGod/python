import requests
from lxml import etree
import urllib.request
import os
import time

base_url = 'https://weheartit.com'
urls = ['https://weheartit.com/inspirations/taylorswift?page={}'.format(str(i)) for i in range(1,2,1)]
base = os.getcwd() + r'\picture'
if not os.path.exists(base):
    os.mkdir(base)

def gotPicture(url,i):
    wbData = requests.get(url).text
    tree = etree.HTML(wbData)
    # images = tree.xpath('//*/img[@height="250" and @width="300"]/@src')
    images = tree.xpath('//*[@class="entry-hover"]/a/@href')
    print(images)
    image_url = []
    for element in images:
        image_url = base_url+element
        # print(image_url)
        wbData = requests.get(image_url).text
        # print(wbData)
        tree = etree.HTML(wbData)
        # //*[@id="content"]/div[2]/div/div/div[1]/div[2]/div/div/div/div/div/div[1]/div/div[2]/a/img
        pictureUrl = tree.xpath('//*[@class="entry-holder"]/a/img/@src')
        # print(pictureUrl)
        file_name = str(i) + '.jpg'
        downloadPath = os.path.join(base,file_name)
        print('downloading   ' + downloadPath)
        print(pictureUrl[0])
        urllib.request.urlretrieve(pictureUrl[0],downloadPath)
        # urllib.request.urlretrieve("https://data.whicdn.com/images/134332180/original.gif",downloadPath)
        i = i + 1
        sleep(2)

if __name__ == '__main__':
    print('########################')
    i = 1
    for url in urls:
        gotPicture(url,i)
        i = i + 24

# image = 'https://data.whicdn.com/images/309352996/superthumb.jpg'
# urllib.request.urlretrieve(image,'1.jpg')
