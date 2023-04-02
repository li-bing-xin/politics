
from datetime import datetime
import json
import sqlite3
from requests import request

API_KEY = 'b861c1e6e7f80f58d3809b86e8a35f74'
BASE_URL = 'http://api.mediastack.com/v1/news'
CATEGORIES = 'politics'

# mediastack这个源只能免费获取到今年开始的新闻
# ！！！注意，每个月只能免费调用500该api

datas = []

def fetch_datas():
    now = datetime.now()

    total = 0
    offset = 0
    page_size = 100  # 允许的最大值为100

    for page in range(1, 200):
        if(offset > total):
            break
        # date=前一年的今天，今年的今天
        url = BASE_URL + '?access_key=' + API_KEY \
            + '&date=' + str(now.year-1) + '-' + str(now.month) + '-' + str(now.day) + ',' + str(now.year) + '-' + str(now.month) + '-' + str(now.day) \
            + '&categories=' + CATEGORIES \
            + '&limit=' + str(page_size) \
            + '&offset=' + str((page - 1) * page_size)
        response = request(method='GET',url=url)
        text = response.text
        res = json.loads(text)
        pages = res['pagination']
        total = pages['total']
        print('mediastack total: ' + str(total))
        offset = pages['offset'] + pages['limit']
        data = res['data']
        datas.extend(data)
        print('page-' + str(page) + ' is done!')

def save_datas():
    conn = sqlite3.connect('../news.db')
    cursor = conn.cursor()

    for data in datas:
        headline = data['title']
        pub_time = data['published_at']
        link = data['url']
        source = data['source']
        country = data['country']
        abstract = data['description']
        content = ''
        standfirst = ''
        api_source = 'mediastack'
        keywords = ''
        word_count = 0

        cursor.execute('''INSERT INTO news VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', \
            (headline,abstract,standfirst,content,pub_time,link,source,api_source,word_count,keywords,country))

    conn.commit()
    conn.close()

fetch_datas()
save_datas()