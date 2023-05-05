# 写一个python服务，读取../../news.db中的news表中的keywords字段，返回给前端
from datetime import datetime
import os
import sqlite3
from flask import Flask, jsonify, redirect, render_template, request, send_from_directory, url_for
from flask_cors import CORS
import pandas as pd

app = Flask(__name__, static_url_path="", static_folder="../web/")
CORS(app)

current_path = os.path.dirname(__file__)
db_path = os.path.join(current_path, "../../news.db")

CENTRIST = "centrist"
LIBERAL = "liberal"
CONSERVATIVE = "conservative"
POSITIVE = "positive"
NEUTRAL = "neutral"
NEGATIVE = "negative"

BLACK_LIST_TOPICS = ['Art', 'Cartoon'] # 奇怪的topic，不需要展示

def stringFirstUpper(string: str):
    return string[0].upper() + string[1:]

# 函数功能：接收一个字符串topic参数，如果topic是一个单词并且是复数形式，就返回单数形式，否则返回原topic
def singularize(topic: str):
    if " " in topic:
        return topic
    if topic.endswith("ies"):
        return topic[:-3] + "y"
    if topic.endswith("s"):
        return topic[:-1]
    return topic


# 这个路由的request url里有一个param是date_range,用来指定最近多少天的数据
@app.route("/api/top_topics", methods=["GET"])
def get_top_topics():
    params = request.args
    date_range = params.get("date_range")
    date_range = int(date_range) if date_range is not None else 7

    # 从数据库中读取最近7天的数据
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM news WHERE pub_time >= date('now', '-{} day')".format(date_range)
    )
    rows = cursor.fetchall()
    topics_count = {}
    for row in rows:
        topic = row[12]
        if topic is not None:
            topic = stringFirstUpper(topic)  # 因为topic的第一个字母不一定是大写，可能导致两个其实是一样的话题分别做了统计
            topic = singularize(topic)
            if topic in BLACK_LIST_TOPICS:
                continue

            is_exist = False
            for key in topics_count:
                if topic.lower() == key.lower():
                    topics_count[key] += 1
                    is_exist = True
                    break
            if not is_exist:
                topics_count[topic] = 1

    # 将数据按照出现次数排序,并且只取前100个
    topics_count = sorted(topics_count.items(), key=lambda x: x[1], reverse=True)[:100]
    # 将数据转换成前端需要的格式
    topics_count = [{"name": item[0], "count": item[1]} for item in topics_count]
    return jsonify(topics_count)


# 获取最近一年内，每个月里的top 20 topics
@app.route("/api/top_topics_by_month", methods=["GET"])
def get_top_topics_by_month():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # 循环12次，每次查询一个月的数据
    topics_count = {}
    for i in range(12):
        cursor.execute(
            "SELECT * FROM news WHERE pub_time >= date('now', '-{} month') AND pub_time < date('now', '-{} month')".format(
                i + 1, i
            )
        )
        topics_count_one_month = {}
        rows = cursor.fetchall()
        for row in rows:
            topic = row[12]
            if topic is not None:
                topic = stringFirstUpper(topic)  # 因为topic的第一个字母不一定是大写，可能导致两个其实是一样的话题分别做了统计
                topic = singularize(topic)
                if topic in BLACK_LIST_TOPICS:
                    continue

                is_exist = False
                for key in topics_count_one_month:
                    if topic.lower() == key.lower():
                        topics_count_one_month[key] += 1
                        is_exist = True
                        break
                if not is_exist:
                    topics_count_one_month[topic] = 1

            # 将数据按照出现次数排序,并且只取前20个
        topics_count_one_month = sorted(
            topics_count_one_month.items(), key=lambda x: x[1], reverse=True
        )[:20]
        # 将数据转换成前端需要的格式
        topics_count_one_month = [
            {"name": item[0], "count": item[1]} for item in topics_count_one_month
        ]

        # 计算往前数i个月的年份和月份
        now = datetime.now()
        year = now.year
        month = now.month
        for i in range(i):
            month -= 1
            if month == 0:
                month = 12
                year -= 1

        topics_count[
            str(year) + "-" + (str(month) if month >= 10 else "0" + str(month))
        ] = topics_count_one_month

    return jsonify(topics_count)


# 获取所有统计数据概览
@app.route("/api/statistic", methods=["GET"])
def get_statistic():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 查询news表中所有新闻的source的个数
    cursor.execute("SELECT COUNT(DISTINCT source) FROM news")
    source_count = cursor.fetchone()[0]

    # 查询news表中所有新闻的数量
    cursor.execute("SELECT COUNT(*) FROM news")
    news_count = cursor.fetchone()[0]

    # 查询news表中所有新闻的analyzed_topic的个数
    cursor.execute("SELECT COUNT(DISTINCT analyzed_topic) FROM news")
    topic_count = cursor.fetchone()[0]

    cursor.close()

    return jsonify(
        {
            "source_count": source_count,
            "news_count": news_count,
            "topic_count": topic_count,
        }
    )


# 获取top 20话题的媒体bias、sentiment统计
@app.route("/api/bias_and_sentiment_statistic", methods=["GET"])
def get_bias_and_sentiment_statistic():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 查出news表中所有的source字段并去重
    cursor.execute("SELECT DISTINCT source FROM news")

    sources = cursor.fetchall()

    # 取出source字段的值
    sources = [source[0] for source in sources]

    cursor.execute("SELECT analyzed_topic, analyzed_sentiment, analyzed_bias, source FROM news")
    rows = cursor.fetchall()
    res = {}

    # 统计top 20 话题的bias和sentiment的个数
    for row in rows:
        topic = row[0]
        sentiment = row[1]
        bias = row[2]
        source = row[3]

        if bias == "radical":
            bias = "liberal"

        if source is not None:

            if source not in res:
                res[source] = {
                    "bias": {
                        CENTRIST: 0,
                        LIBERAL: 0,
                        CONSERVATIVE: 0,
                    },
                    "sentiment": {POSITIVE: 0, NEUTRAL: 0, NEGATIVE: 0},
                    "count": 0,
                }

            bias_valid = [CENTRIST, LIBERAL, CONSERVATIVE]
            sentiment_valid = [POSITIVE, NEUTRAL, NEGATIVE]

            if bias is not None and bias in bias_valid:
                res[source]["bias"][bias] += 1
            if sentiment is not None and sentiment in sentiment_valid:
                res[source]["sentiment"][sentiment] += 1
            res[source]["count"] += 1

    # 将数据按照出现次数排序,并且只取前20个
    res = sorted(res.items(), key=lambda x: x[1]["count"], reverse=True)[:20]

    return jsonify(res)


# 统计美国各个州的新闻数量
@app.route("/api/news_by_state", methods=["GET"])
def get_news_by_state():
    # 数据库中每条数据都有一个state字段，它的值是字符串的None或者是一个美国州的名字，例如"California"，请统计出每个州的新闻数量和Top 10热门话题
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT analyzed_topic, analyzed_state FROM news WHERE pub_time >= date('now', '-365 day')"
    )
    rows = cursor.fetchall()
    res = {}

    # 统计top 20 话题的bias和sentiment的个数
    for row in rows:
        topic = row[0]
        state: str = row[1]

        if state == 'None' or state is None:
            continue

        # 去掉state中的所有引号
        state = state.replace("'", "").replace('"', "").replace('\n', ",").replace('and', ",")
        states = state.split(',')

        for state in states:
            state = state.strip()
            if state not in res:
                res[state] = {
                    "news_count": 0,
                    "topics": {},
                }

            if topic is not None:
                topic = stringFirstUpper(topic)   # 因为topic的第一个字母不一定是大写，可能导致两个其实是一样的话题分别做了统计
                topic = singularize(topic)
                if topic in BLACK_LIST_TOPICS:
                    continue

                res[state]["news_count"] += 1
                res[state]["topics"][topic] = res[state]["topics"].get(topic, 0) + 1

    # 排序res[state]["topics"]
    res = {state: {"news_count": res[state]["news_count"], "topics": sorted(res[state]["topics"].items(), key=lambda x: x[1], reverse=True)[:10]} for state in res}

    return jsonify(res)


# 通过历史数据预测下个月的top 10话题
@app.route("/api/predict_next_month_top_topics_10", methods=["GET"])
def get_predict():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # 循环12次，每次查询一个月的数据
    topics_count = {}
    for i in range(12):
        cursor.execute(
            "SELECT * FROM news WHERE pub_time >= date('now', '-{} month') AND pub_time < date('now', '-{} month')".format(
                i + 1, i
            )
        )
        topics_count_one_month = {}
        rows = cursor.fetchall()
        for row in rows:
            topic = row[12]
            if topic is not None:
                topic = stringFirstUpper(topic)  # 因为topic的第一个字母不一定是大写，可能导致两个其实是一样的话题分别做了统计
                topic = singularize(topic)
                if topic in BLACK_LIST_TOPICS:
                    continue

                is_exist = False
                for key in topics_count_one_month:
                    if topic.lower() == key.lower():
                        topics_count_one_month[key] += 1
                        is_exist = True
                        break
                if not is_exist:
                    topics_count_one_month[topic] = 1

            # 将数据按照出现次数排序,并且只取前20个
        topics_count_one_month = sorted(
            topics_count_one_month.items(), key=lambda x: x[1], reverse=True
        )[:20]
        # 将数据转换成前端需要的格式
        topics_count_one_month = [
            {"name": item[0], "count": item[1]} for item in topics_count_one_month
        ]

        # 计算往前数i个月的年份和月份
        now = datetime.now()
        year = now.year
        month = now.month
        for i in range(i):
            month -= 1
            if month == 0:
                month = 12
                year -= 1

        topics_count[
            str(year) + "-" + (str(month) if month >= 10 else "0" + str(month))
        ] = topics_count_one_month


    json_data = topics_count

    # 将数据转换为DataFrame格式
    data = {}
    for month in json_data.keys():
        for item in json_data[month]:
            name = item['name']
            count = item['count']
            if name in data:
                data[name].append((month, count))
            else:
                data[name] = [(month, count)]

    # 将数据按照count排序
    sorted_data = sorted(data.items(), key=lambda x: x[1][-1][1], reverse=True)

    # 创建一个滑动窗口
    window_size = 3
    window = []
    for i in range(window_size):
        window.append(sorted_data[i][0])

    # 预测未来一个月的top20新闻热点话题
    next_month = pd.to_datetime(list(json_data.keys())[-1]) + pd.DateOffset(months=1)
    next_month_str = next_month.strftime('%Y-%m')
    predictions = []
    for item in sorted_data:
        if item[0] not in window:
            window.pop(0)
            window.append(item[0])
            predictions.append(item[0])
        if len(predictions) == 20:
            break

    # 输出预测结果
    arr = []
    for i, topic in enumerate(predictions):
        arr.append(topic)

    return jsonify(arr)


if __name__ == "__main__":
    app.run(port=3000, host="0.0.0.0")