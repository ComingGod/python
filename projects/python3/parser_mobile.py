from lxml import  etree
from bs4 import BeautifulSoup
import requests

url = 'https://cn.tripadvisor.com/Attractions-g60763-Activities-New_York_City_New_York.html'
# url = 'https://cn.tripadvisor.com/Attractions-g60763-Activities-c47-oa420-New_York_City_New_York.html#FILTERED_LIST'
headers = {
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'
}
mb_data = requests.get(url,headers=headers).text
soup = BeautifulSoup(mb_data,'lxml')
print (soup)
images = soup.select('div.prw_rup.prw_common_centered_thumbnail > div > div > img')
print(images)



data = []
for image in images:
    info = {
        'image':image.get('src')
    }
    data.append(info)
    print (info)
print(data)
# taplc_mobile_attraction_coverpage_0 > div.coverpage > div:nth-child(1) > div > div > div > div:nth-child(1) > a > div > div.prw_rup.prw_common_centered_thumbnail > div > div
#
# taplc_mobile_attraction_coverpage_0 > div.coverpage > div:nth-child(1) > div > div > div > div:nth-child(1) > a > div > div.prw_rup.prw_common_centered_thumbnail > div > div

