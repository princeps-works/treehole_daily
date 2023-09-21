import datetime
import logging
import os
from world_cloud import texts_2_word_cloud, get_text
from integration.lark import send
import get_words

def main():
    today = datetime.date.today()
    delta = datetime.timedelta(days=-1)
    yesterday = today + delta
    newspaper = news_drawing()
    newspaper.to_file(f"./data/output/{yesterday}/newspaper.png")
    with open(f"./data/output/{yesterday}/newspaper.png", "rb") as f:
        send(f)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
