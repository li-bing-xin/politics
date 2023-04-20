from init_db import init_db
from guardian.fetch import fetch_datas as fetch_guardian, save_datas as save_guardian
from mediastack.fetch import fetch_datas as fetch_mediastack, save_datas as save_mediastack
from nytimes.fetch import fetch_datas as fetch_nytimes, save_datas as save_nytimes


def fetch_data():

    # 初始化数据库
    init_db()

    # 从guardian获取数据并保存
    fetch_guardian()
    save_guardian()

    # 从mediastack获取数据并保存
    fetch_mediastack()
    save_mediastack()

    # 从nytimes获取数据并保存
    fetch_nytimes()
    save_nytimes()

fetch_data()