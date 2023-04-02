

import os
from requests import request
from datetime import datetime

API_KEY = 'O7R3Sk5cdbpDAvAlpQGlO7bHk6NlDVPH'
BASE_URL = 'https://api.nytimes.com/svc/archive/v1'

# 删除data以及data下的所有文件
if os.path.exists('data'):
    os.system('rm -rf data')

# 得到2022年每个月的文章列表
years = list([2022, 2023])

os.mkdir('data')
for year in years:
    os.mkdir('data/' + str(year))
    now = datetime.now()
    month_range = range(1, 13) if year != now.year else range(1, now.month + 1)
    for month in month_range:
        url = BASE_URL + '/' + str(year) + '/' + str(month) + '.json?api-key=' + API_KEY
        response = request(method='GET',url=url)
        text = response.text
        with open('data/' + str(year) + '/' + str(month) + '.json', 'w', encoding='utf-8') as f:
            f.write(text)
            print(str(year) + '-' + str(month) + ' is done!')