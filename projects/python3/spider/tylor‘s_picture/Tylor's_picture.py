import requests
from lxml import etree
import urllib.request
import os

urls = ['https://weheartit.com/inspirations/taylorswift?page={}'.format(str(i)) for i in range(1,21,1)]
base = os.getcwd() + r'\picture'
if not os.path.exists(base):
    os.mkdir(base)

def gotPicture(url,i):
    wbData = requests.get(url).text
    tree = etree.HTML(wbData)
    images = tree.xpath('//*/img[@height="250" and @width="300"]/@src')
    print(images)
    for image in images:
        file_name = str(i) + '.jpg'
        downloadPath = os.path.join(base,file_name)
        print('downloading   ' + downloadPath)
        urllib.request.urlretrieve(image,downloadPath)
        i = i + 1

if __name__ == '__main__':
    print('########################')
    i = 1
    for url in urls:
        gotPicture(url,i)
        i = i + 24

# image = 'https://data.whicdn.com/images/309352996/superthumb.jpg'
# urllib.request.urlretrieve(image,'1.jpg')
