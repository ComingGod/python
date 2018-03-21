from bs4 import BeautifulSoup
import requests

url = 'https://cn.tripadvisor.com/Attractions-g60763-Activities-New_York_City_New_York.html'
wb_data = requests.get(url).content
soup = BeautifulSoup(wb_data, 'lxml')
titles = soup.select('div.listing_title > a')
images  = soup.select('img[width="180"]')
print (images)


for title,image in zip(titles,images):
    data = {
        'title': title.get_text(),
        'image': image.get('src')
    }
print(data)



# html='''
# <a class="css" href="http://example.com/test" id="test"><!--test --></a>
# '''
# bs=BeautifulSoup(html,"html.parser")
# print(bs.a.get('href'))
# print (bs.a.string)

