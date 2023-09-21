import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import pyfiglet
from cowsay import cowsay
import random
from world_cloud import get_text_
##get words
def get_text_(db_url: str, sql: str):
    engine = sqlalchemy.create_engine(db_url)
    sql = sqlalchemy.text(sql)
    with engine.connect() as conn:
        df = pd.read_sql(sql=sql, con=conn)
    return df.to_numpy().tolist()
today = datetime.date.today()
delta = datetime.timedelta(days=-1)
yesterday = today + delta
sql2 = f"select content,`like`,hole_id from fduhole.moderator_floor where created_at between '{yesterday}' and '{today}' and deleted = 0;"
sql3 = f"select dau from fduhole.moderator_dau LIMIT 1 ;"
sql4 = f"select mau from fduhole.moderator_mau LIMIT 1 ;"
text = get_text(os.environ.get("DB_URL"),sql2)
dau = get_text(os.environ.get("DB_URL"),sql3)
mau = get_text(os.environ.get("DB_URL"),sql4) 
sorted_text = sorted(text, key = lambda x:x[1], reverse = True)[:5]
dau_str = '日活量：'
mau_str = '月活量：'
text_setype = []
count_line = 1
for st in sorted_text:
    sp = st[0]
    #st_all = ''.join(sp)
    st_setype = ''
    i = 1
    for wd in sp:
        if wd == '\n':
            st_setype += wd
            count_line += 1
            i = 1
        elif i%30 == 0 or i%31 == 0:
            st_setype += wd+'\n'
            count_line += 1
            i = 1
        elif 0x4e00 <= ord(wd) <= 0x9fa5 or 0xFF01 <= ord(wd) <= 0xFF5E:
            st_setype += wd
            i += 2
        else:
            st_setype += wd
            i += 1
    text_setype += [st_setype]
for d in dau:
    dau_str += str(d[0])
    
for m in mau:
    mau_str += str(m[0])
body_text1 = ''
for i,j,k in zip(sorted_text, range(1,6), text_setype):
    body_text1 += "No.{} \n点赞数为{}，来自洞#{}:\n".format(j,i[1],i[2]) + k + '\n\n'
    count_line += 4
choice ="armadillo  seahorse  daemon  moose bud-frogs stegosaurus llama happy-whale  satanic clippy taxi milk elephant  blowfish small dragon tux octopus fat-banana  cheese surgery elephant-in-snake banana sheep kitten  default turtle frogs bunny stimpy lobster  elephant2 whale hellokitty cower three-eyes moofasa  flaming-sheep  koala dragon-and-cow TuxStab owl  head-in  meow eyes bill-the-cat  kitty  mutilated ghost cat supermilker  lollerskates"
mascot = choice.split()
today_mascot = random.choice(mascot) 
message = "到此为止啦   *:\(￣︶￣)/:*   "
text_mascot=cowsay(message, cow=today_mascot)
image_path1 = "./data/output/{yesterday}.png"
im1 = Image.open(image_path1)
image_path2 = "./background2.png"
image_path3 = "./treehole.png"
im2 = Image.open(image_path2)
im3 = Image.open(image_path3)
text_command=''
wc，command = texts_2_word_cloud(text1)
for w,n in command:
    text_command += "关键词“{}”出现了 {} 次".format(w,n)+'\n'
