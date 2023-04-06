# 遍历news.db中的news表中的所有数据，对每条数据提炼关键词，将结果存入keywords字段中
import json
import sqlite3
import openai

openai.api_key = "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"


def query_openai(string: str):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Extract keywords from this text:\n\n" + string + "\n\nKeywords: ",
        temperature=0.5,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.8,
        presence_penalty=0.0,
    )
    response = str(response)
    response = json.loads(response)
    # 取出response中的choices字段中的text字段
    keywords = response["choices"][0]["text"]
    # 把keywords字符串用逗号分割成列表，并且去掉每个元素两边的空格
    keywords = [keyword.strip() for keyword in keywords.split(",")]
    # 把列表转换成字符串
    keywords = ",".join(keywords)
    return keywords


def analyze():
    conn = sqlite3.connect("./news.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news limit 3 offset 0")
    rows = cursor.fetchall()

    for row in rows:
        # 取出每条数据的各个字段
        id = row[0]
        headline = row[1]
        abstract = row[2]
        lead_paragraph = row[3]
        content = row[4]
        pub_time = row[5]
        link = row[6]
        source = row[7]
        api_source = row[8]
        word_count = row[9]
        keywords = row[10]
        country = row[11]

        if keywords == "":
            continue
        else:
            query_openai(content or lead_paragraph or abstract or headline)

    conn.close()


analyze()
