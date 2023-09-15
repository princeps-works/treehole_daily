import logging
import os
from collections import Counter

import jieba
import sqlalchemy
from wordcloud import WordCloud
import pandas as pd


def get_text(db_url: str, sql: str):
    engine = sqlalchemy.create_engine(db_url)
    sql = sqlalchemy.text(sql)
    with engine.connect() as conn:
        df = pd.read_sql(sql=sql, con=conn)
    return df.to_numpy()


def check_contain_chinese(check_str):
    for ch in check_str:
        if "\u4e00" <= ch <= "\u9fff":
            return True
    return False


def texts_2_word_cloud(texts: list[str]) -> WordCloud:
    logging.info("Start to generate word cloud")
    logging.info("Loading custom dictionary")

    for i in os.listdir("./data/dict"):
        with open(f"./data/dict/{i}", "r", encoding="utf8") as f:
            jieba.load_userdict(f)

    logging.info("Loading stop words")
    stop_words = []
    for i in os.listdir("./data/stop"):
        with open(f"./data/stop/{i}", "r", encoding="utf8") as f:
            stop_words += f.readlines()
    stop_words = [w.strip() for w in stop_words]
    stop_words = set(stop_words)

    logging.info("Cutting words")
    words = []
    for line in texts:
        words += jieba.lcut(line, cut_all=False)
    counter = Counter()
    for word in words:
        if (
            len(word) > 1
            and word not in stop_words
            and (word.isalnum() or check_contain_chinese(word))
        ):
            counter[word] += 1
    sorted_dict = dict(sorted(counter.items(), key=lambda item: item[1], reverse=True))
    
    logging.info("Generating word cloud")
    return WordCloud(
        font_path="./data/font/SourceHanSansSC-Regular.otf",
        background_color="white",
        width=4096,
        height=2160,
        margin=10,
    ).generate_from_frequencies(counter) ,sorted_dict.items()[:5]
