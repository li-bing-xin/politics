

import json
import os
import sqlite3
from time import sleep
from requests import request
from datetime import datetime

API_KEY: str = 'O7R3Sk5cdbpDAvAlpQGlO7bHk6NlDVPH'


def fetch_datas():
    print('nytimes start')

    current_path = os.path.dirname(__file__)
    data_path = os.path.join(current_path, "./data")
    if not os.path.exists(data_path):
        os.mkdir(data_path)

    BASE_URL = 'https://api.nytimes.com/svc/archive/v1'

    year = datetime.now().year
    years = list([year - 1, year])

    for year in years:
        dir_path = os.path.join(current_path, 'data/' + str(year))

        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        now = datetime.now()
        month_range = range(1, 13) if year != now.year else range(1, now.month + 1)
        for month in month_range:
            path = os.path.join(current_path, 'data/' + str(year) + '/' + str(month) + '.json')

            # 如果文件存在并且年月不是当前的年月，则跳过
            if os.path.exists(path) and not (year == now.year and month == now.month):
                continue

            url = BASE_URL + '/' + str(year) + '/' + str(month) + '.json?api-key=' + API_KEY
            response = request(method='GET',url=url)
            text = response.text
            with open(path, 'w', encoding='utf-8') as f:
                f.write(text)
                print(str(year) + '-' + str(month) + ' is done!')
                sleep(60)



def save_datas():
    current_path = os.path.dirname(__file__)
    db_path = os.path.join(current_path, "../news.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 读取data目录，并循环下面的所有文件
    data_dir = os.path.join(current_path, './data')
    for dir in os.listdir(data_dir):

        year_dir = os.path.join(current_path, './data/'+ dir)
        for filename in os.listdir(year_dir):
            # 从data目录的json里读取并写入数据

            with open(os.path.join(current_path, './data/'+ dir + '/' + filename), 'r', encoding = 'utf-8') as f:
                data = json.load(f)


                # 如果response字段不存在，就跳过
                if 'response' not in data:
                    print(data['response'] is None)
                    continue

                # 获取response列表
                docs = data['response']['docs']
                # 过滤出web_url字段中包含 '/politics/' 的所有数据
                docs = list(filter(lambda x: '/politics/' in x['web_url'], docs))

                print('共有%d条数据' % len(docs))

                # 循环遍历response列表
                for item in docs:
                    # 获取title字段
                    content = ''
                    link = item['web_url']
                    abstract = item['abstract']
                    lead_paragraph = item['lead_paragraph']
                    # item['keywords']的值是list，使用json库的方法将其转为字符串
                    keywords = json.dumps(item['keywords'])
                    source = item['source']
                    pub_time = item['pub_date']
                    word_count = item['word_count']
                    api_source = 'nytimes'
                    # 如果item中存在headline字段并且值为array，取第一个元素的main字段赋给headline变量，否则取headline字段的main字段赋给headline变量
                    headline = item['headline']['main'] if isinstance(item['headline'], dict) else item['headline'][0]['main']
                    country = ''

                    # 在数据库中查询，如果已经存在，就不再插入
                    cursor.execute('''SELECT * FROM news WHERE headline=? AND link=?''', (headline,link,))

                    if cursor.fetchone() is None:
                        cursor.execute('''INSERT INTO news VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', \
                            (headline,abstract,lead_paragraph,content,pub_time,link,source,api_source,word_count,keywords,country,None,None,None,None,None))

    conn.commit()
    conn.close()
