import requests
from pyquery import PyQuery as pq
import pymongo
import time

clien=pymongo.MongoClient(host='改成自己的')
db=clien.To_the_guest
coll=db.Housing_datas

headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

def Housing_informations(url):
    sponse=requests.get(url,headers=headers).text
    doc=pq(sponse)
    information=doc('.houseInfo-detail-list').items()
    for i in information:

        data={
            '所属小区':i.find('.houseInfo-content a').text(),
            '具体位置':i.find('.loc-text').text()
        }
        return data



#爬取房屋具体信息的URL
def Crawl_home_URL(page):

    URL='https://guilin.anjuke.com/sale/p{}-rd1/'.format(page)

    Sponse=requests.get(URL,headers=headers).text
    #print(Sponse)
    doc=pq(Sponse)
    link=doc('.list-item').items()
    for i in link:

        The_URL_of_the_building=i.find('a').attr('href')
        #价钱
        The_price=i.find('.price-det').text()
        #房屋图片
        House_pictures=pq(i.find('.item-img').html()).find('img').attr('src')

        #多少钱一平米
        How_much_is_a_square_meter=i.find('.unit-price').text()
        #房屋信息
        Housing_information=i.find('.details-item').text()
        Housing_data={
            '房屋信息':Housing_information,
            '房屋价钱':The_price,
            '多少钱一平米':How_much_is_a_square_meter,
            '房屋图片':House_pictures,
            '具体的房屋信息':The_URL_of_the_building
        }



        ddata=Housing_informations(The_URL_of_the_building)
        z = Housing_data.copy()
        z.update(ddata)
        coll.insert_one(z)
        print(z)

for i in range(1,51):
    Crawl_home_URL(i)
