import os
import sqlite3
import json

def save_datas():
    conn = sqlite3.connect('../news.db')
    cursor = conn.cursor()

    # 读取data目录，并循环下面的所有文件
    for dir in os.listdir('./data'):
        for filename in os.listdir('./data/'+ dir):
            # 从data目录的json里读取并写入数据
            with open('./data/'+ dir + '/' + filename, 'r', encoding = 'utf-8') as f:
                data = json.load(f)

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
                    standfirst = item['lead_paragraph']
                    # item['keywords']的值是list，使用json库的方法将其转为字符串
                    keywords = json.dumps(item['keywords'])
                    source = item['source']
                    pub_time = item['pub_date']
                    word_count = item['word_count']
                    api_source = 'nytimes'
                    # 如果item中存在headline字段并且值为array，取第一个元素的main字段赋给headline变量，否则取headline字段的main字段赋给headline变量
                    headline = item['headline']['main'] if isinstance(item['headline'], dict) else item['headline'][0]['main']
                    country = ''

                    # 将上面的所有字段写入SQLite数据库
                    cursor.execute('''INSERT INTO news VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', \
                        (headline,abstract,standfirst,content,pub_time,link,source,api_source,word_count,keywords,country,))

            conn.commit()

    conn.close()

save_datas()