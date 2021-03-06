import datetime
import json

import requests
import time
import pymongo
import random
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import asyncio

base_url = 'https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/common-api/organization/children?pid='
# 模拟用户访问
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Mobile Safari/537.36 Edg/102.0.1245.30"
}
# 创建数据库
client = pymongo.MongoClient('localhost', 27017)
mydb = client.dxx
dxx_zj = mydb.dxx_zj
sleeptime = random.randint(2, 8)
t = ['N0019', 'N0013']
try:
    for u in t:
        url = base_url + u
        response = requests.get(url=url, headers=headers)
        response.encoding = response.apparent_encoding
        obj = response.json()
        response.close()
        for item in obj['result']:
            danwei1 = item['title'][:-2]
            id1 = item['id']
            url1 = base_url + id1
            response1 = requests.get(url=url1, headers=headers)
            response1.encoding = response1.apparent_encoding
            response1.close()
            obj1 = response1.json()
            for item1 in obj1['result']:
                danwei2 = item1['title']
                id2 = item1['id']
                url2 = base_url + id2
                response2 = requests.get(url=url2, headers=headers)
                response2.encoding = response2.apparent_encoding
                response2.close()
                obj2 = response2.json()
                for item2 in obj2['result']:
                    danwei3 = item2['title']
                    id3 = item2['id']
                    dxx_zj.insert_one({
                        "id1": id1,
                        "school": danwei1,
                        "id2": id2,
                        "college": danwei2,
                        "id3": id3,
                        "class": danwei3
                    })
                    print(f'{danwei1}-{danwei2}-{danwei3}-已写入数据库！')
                print(f'{danwei1}-{danwei2}-已全部写入数据库！')
                time.sleep(sleeptime)
            print(f'{danwei1}-已全部写入数据库！')
            time.sleep(sleeptime)
except Exception as result:
    print(result)
    dxx_zj.insert_one({
        "id1": 'empty',
        "school": 'empty',
        "id2": 'empty',
        "college": 'empty',
        "id3": 'empty',
        "class": 'empty'
    })


