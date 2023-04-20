from datetime import datetime
import json
import os
import sqlite3
from requests import request


API_KEY: str = 'a1d9129e-4b9f-4ece-8365-6062835929a2'

datas = []

def fetch_datas():
    BASE_URL = 'https://content.guardianapis.com/search'

    now = datetime.now()
    year = now.year

    total = 0
    offset = 0
    page_size = 100 # 允许的最大值为100

    for page in range(1, 200):
        if(offset > total):
            break
        # from-date是前一年的今天，to-date是今年的今天
        url = BASE_URL + '?q=politic&format=json' \
            + '&from-date=' + str(year-1) + '-' + str(now.month) + '-' + str(now.day) \
            + '&to-date=' + str(year) + '-' + str(now.month) + '-' + str(now.day) \
            + '&api-key=' + API_KEY \
            + '&show-fields=wordcount,headline,standfirst,body' \
            + '&page=' + str(page) + '&page-size=' + str(page_size)
        response = request(method='GET',url=url)
        text = response.text
        res = json.loads(text)
        response = res['response']
        total = response['total']
        print('guardian total: ' + str(total))
        offset = response['currentPage'] * response['pageSize']
        data = response['results']
        datas.extend(data)
        print('page-' + str(page) + ' is done!')

def save_datas():
    current_path = os.path.dirname(__file__)
    db_path = os.path.join(current_path, "../news.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for data in datas:
        headline = data['fields']['headline']
        content = data['fields']['body']
        pub_time = data['webPublicationDate']
        link = data['webUrl']
        source = 'The Guardian'
        country = ''
        abstract = ''
        # 如果standfirst不存在，就赋予空字符串
        lead_paragraph = data['fields']['standfirst'] if 'standfirst' in data['fields'] else ''
        api_source = 'guardian'
        keywords = ''
        word_count = int(data['fields']['wordcount'])

        # 在数据库中查询，如果已经存在，就不再插入
        cursor.execute('''SELECT * FROM news WHERE headline=? AND link=?''', (headline,link,))

        if cursor.fetchone() is None:
            cursor.execute('''INSERT INTO news VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', \
                (headline,abstract,lead_paragraph,content,pub_time,link,source,api_source,word_count,keywords,country,None,None,None,None,None))

    conn.commit()
    conn.close()