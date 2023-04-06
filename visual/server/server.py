# 写一个python服务，读取../../news.db中的news表中的keywords字段，返回给前端
import sqlite3
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def get_keywords():
    conn = sqlite3.connect("../../news.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news")
    rows = cursor.fetchall()
    conn.close()
    return rows


@app.route("/api/data", methods=["GET"])
def get_keywords_api():
    keywords = get_keywords()
    return jsonify(keywords)


if __name__ == "__main__":
    app.run(port=3000, host="127.0.0.1")
