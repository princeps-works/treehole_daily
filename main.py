import datetime
import logging
import os
from world_cloud import texts_2_word_cloud, get_text
from integration.lark import send


def main():
    today = datetime.date.today()
    delta = datetime.timedelta(days=-1)
    yesterday = today + delta

    sql1 = f"select content from fduhole.floor where updated_at between '{yesterday}' and '{today}' and deleted = 0"
    sql2 = f"select content,like,hole_id from fduhole.floor where created_at between '{yesterday}' and '{today}' and deleted = 0"
    text1 = get_text(os.environ.get("DB_URL"), sql1) 
    text2 = get_text(os.environ.get("DB_URL"), sql2) 
    wc，command = texts_2_word_cloud(text1)
    text_command = ''
    for wds in command:
        text_command += '
    wc.to_file(f"./data/output/{yesterday}.png")
    
    with open(f"./data/output/{yesterday}.png", "rb") as f:
        send(f)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
