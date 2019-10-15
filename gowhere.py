import requests
from pyquery import PyQuery as pq
from fake_useragent import UserAgent
import time
import random
import pymongo

clien=pymongo.MongoClient(host='改成自己的数据库IP')
db=clien.trave_guide
coll=db.text

ua=UserAgent()

headers={
    'User-Agent':ua.random
}

def request_HTML(page):
    URL='http://travel.qunar.com/travelbook/list.htm?page={}&order=hot_heat'.format(page)
    sponse=requests.get(URL,headers=headers).text
    return sponse

def Parsing_data(html):
    doc=pq(html)
    Comprehensive_content=doc('.list_item ').items()
    data={}

    for i in Comprehensive_content:
        data = {}
        #获取标题
        The_title=i.find('.tit a').text()

        #出发时间
        Departure_time=i.find('.date').text()

        #共几天
        For_a_few_days=i.find('.days').text()

        #一个有几张旅行照片
        How_many_travel_photos=i.find('.photo_nums').text()

        #途径
        way=i.find('.places').text()

        #人均
        Per_capita=i.find('.fee').text()

        #浏览人数
        Number_of_visitors=i.find('.iconfont').text()

        data['标题'] = The_title
        data['出发时间'] = Departure_time
        data['共几天'] = For_a_few_days
        data['几张照片'] = How_many_travel_photos
        data['途径'] = way
        data['人均'] = Per_capita
        data['浏览人数']=Number_of_visitors

        coll.insert_one(data)
        print(data)




for i in range(1,200):
    Parsing_data(request_HTML(i))

    time.sleep(random.randint(1))
print('已全部保存到数据库中 请查看...')
