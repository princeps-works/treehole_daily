import datetime
import logging
import os
from world_cloud import texts_2_word_cloud, get_text
from integration.lark import send


def main():
    today = datetime.date.today()
    delta = datetime.timedelta(days=-1)
    yesterday = today + delta

    sql = f"select content from fduhole.floor where updated_at between '{yesterday}' and '{today}' and deleted = 0"

    text = get_text(os.environ.get("DB_URL"), sql)
    wc = texts_2_word_cloud(text)
    wc.to_file(f"./data/output/{yesterday}.png")
    with open(f"./data/output/{yesterday}.png", "rb") as f:
        send(f)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
