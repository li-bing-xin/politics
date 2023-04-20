import os
import sqlite3


def init_db():
    # 获取当前所在目录
    current_path = os.path.dirname(__file__)
    db_path = os.path.join(current_path, "news.db")

    # 如果数据库文件存在，直接返回
    if os.path.exists(db_path):
        return

    conn = sqlite3.connect(db_path)
    print("数据库打开成功")
    c = conn.cursor()

    # 删除news表并重新创建
    # c.execute('''DROP TABLE news''')

    c.execute(
        """CREATE TABLE news
              (id                   INTEGER     PRIMARY KEY     AUTOINCREMENT,
              headline              TEXT        NOT NULL,
              abstract              TEXT        NOT NULL,
              lead_paragraph        TEXT,
              content               TEXT,
              pub_time              TEXT,
              link                  TEXT        NOT NULL,
              source                TEXT,
              api_source            TEXT,
              word_count            INT,
              keywords              TEXT,
              country               TEXT,
              analyzed_topic        TEXT,
              analyzed_keywords     TEXT,
              analyzed_sentiment    TEXT,
              analyzed_bias         TEXT,
              analyzed_state        TEXT
              );"""
    )
    print("数据表创建成功")

    conn.commit()
    conn.close()
