import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import pyfiglet
from cowsay import cowsay
import random
import world_cloud 
import os
def news_drawing():
    ##get words
    today = datetime.date.today()
    delta = datetime.timedelta(days=-1)
    yesterday = today + delta
    sql1 = f"select content from fduhole.floor where updated_at between '{yesterday}' and '{today}' and deleted = 0"
    sql2 = f"select content,`like`,hole_id from fduhole.moderator_floor where created_at between '{yesterday}' and '{today}' and deleted = 0;"
    sql3 = f"select dau from fduhole.moderator_dau LIMIT 1 ;"
    sql4 = f"select mau from fduhole.moderator_mau LIMIT 1 ;"
    text_two_words = get_text(os.environ.get("DB_URL"),sql1).tolist().flatten()
    text = get_text(os.environ.get("DB_URL"),sql2).tolist()
    dau = get_text(os.environ.get("DB_URL"),sql3).tolist()
    mau = get_text(os.environ.get("DB_URL"),sql4).tolist()
    sorted_text = sorted(text, key = lambda x:x[1], reverse = True)[:5]
    dau_str = '日活量：'
    mau_str = '月活量：'
    text_setype = []
    count_line = 1
    for st in sorted_text:
        sp = st[0]
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
    text_command=''
    wc，command = texts_2_word_cloud(text_two_words)
    for w,n in command:
        text_command += "关键词“{}”出现了 {} 次".format(w,n)+'\n'
    wc.to_file(f"./data/output/{yesterday}/wordscloud.png")
    image_path1 = "./data/output/{yesterday}/wordscloud.png"
    im1 = Image.open(image_path1)
    image_path2 = "./background2.png"
    image_path3 = "./treehole.png"
    im2 = Image.open(image_path2)
    im3 = Image.open(image_path3)

    
    ##setting   
    ImageFont.load_default()
    page_width = 580  # 页面宽度，以像素为单位
    page_height = count_line*30 + 2190  # 页面高度，以像素为单位
    background_color = (255, 255, 255)  # 页面背景颜色
    im1_new = im1.resize((500,400), box=None, reducing_gap=None)
    im2_new = im2.resize((580,page_height), box=None, reducing_gap=None)
    im3_new = im3.resize((580,500), box=None, reducing_gap=None)
    title_text1 = "树洞日报"
    title_text2 = "\n \n Treehole Daily"
    title_font1 = ImageFont.truetype(".\汉仪尚巍手书.ttf",120)  # 使用自定义字体
    title_font2 = ImageFont.truetype('.\汉仪闫锐敏行楷简.ttf',80)
    subtitle_font = ImageFont.truetype(".\包图小白体.ttf",60)
    body_font1 = ImageFont.truetype(".\方正盛世楷书简体_中.TTF",30)
    mascot_font1 = ImageFont.truetype(".\汉仪趣黑.otf",25)
    mascot_font2 = ImageFont.truetype(".\包图小白体.ttf",40)
    title_color = (0, 0, 0)  # 白色
    mascot_color = (128, 0, 128)
    
    
    ##drawing picture
    page = Image.new('RGB', (page_width, page_height), background_color)
    draw = ImageDraw.Draw(page)
    page.paste(im2_new, (0,0))
    draw.text((30,50), title_text1, title_color,font=title_font1)
    draw.text((30,50), title_text2, title_color,font=title_font2)
    draw.text((30,300), dau_str, title_color,font=body_font1)
    draw.text((30,350), mau_str, title_color,font=body_font1)
    draw.text((30,420), '一.获赞数TOP5',(0,160,0) ,font=subtitle_font)
    draw.text((50,500), body_text1, title_color,font=body_font1)
    draw.text((30,500+30*(count_line+2)), '二.今日词云', (0,160,0),font=subtitle_font)
    page.paste(im1_new, (50, 500+30*(count_line+5)))
    draw.text((50,500+30*(count_line+19)),text_command,title_color,font=body_font1)
    draw.text((0,500+30*(count_line+25)),text_mascot,title_color,font=mascot_font1)
    draw.text((50,500+30*(count_line+40)),"今日吉祥物："+today_mascot,title_color,font=mascot_font2)
    draw.text((0,510+30*(count_line+41)),'—— '*10,title_color,font=body_font1)
    page.paste(im3_new, (0, 480+30*(count_line+43)))
    return  page
    
