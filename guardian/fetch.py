from datetime import datetime
import json
import sqlite3

from requests import request


BASE_URL = 'https://content.guardianapis.com/search'
API_KEY = 'a1d9129e-4b9f-4ece-8365-6062835929a2'

datas = []

def fetch_datas():
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
    conn = sqlite3.connect('../news.db')
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
        standfirst = data['fields']['standfirst'] if 'standfirst' in data['fields'] else ''
        api_source = 'guardian'
        keywords = ''
        word_count = int(data['fields']['wordcount'])

        cursor.execute('''INSERT INTO news VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', \
            (headline,abstract,standfirst,content,pub_time,link,source,api_source,word_count,keywords,country,))

    conn.commit()
    conn.close()

fetch_datas()
save_datas()