
from datetime import datetime
import json
import os
import sqlite3
from requests import request

API_KEY: str = 'b861c1e6e7f80f58d3809b86e8a35f74'

# mediastack这个源只能免费获取到今年开始的新闻
# ！！！注意，每个月只能免费调用500该api

datas = []

def fetch_datas():
    CATEGORIES = 'politics'
    BASE_URL = 'http://api.mediastack.com/v1/news'

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
    current_path = os.path.dirname(__file__)
    db_path = os.path.join(current_path, "../news.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for data in datas:
        headline = data['title']
        pub_time = data['published_at']
        link = data['url']
        source = data['source']
        country = data['country']
        abstract = data['description']
        content = ''
        lead_paragraph = ''
        api_source = 'mediastack'
        keywords = ''
        word_count = 0

        # 在数据库中查询，如果已经存在，就不再插入
        cursor.execute('''SELECT * FROM news WHERE headline=? AND link=?''', (headline,link,))

        if cursor.fetchone() is None:
            cursor.execute('''INSERT INTO news VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', \
                (headline,abstract,lead_paragraph,content,pub_time,link,source,api_source,word_count,keywords,country,None,None,None,None,None))

    conn.commit()
    conn.close()