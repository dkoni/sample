import requests
from bs4 import BeautifulSoup
from time import sleep
import re
import pandas as pd

# １列目：読み方(ひらがな)
# ２列目：正式名
# ３列目：英語表記
# ４列目：作品名
# ５列目：作品名の英語表記

def kata_to_hira(txt):
    return "".join([chr(ord(ch) - 96) if ("ァ" <= ch <= "ヴ") else ch for ch in txt])

url = 'https://schara.sunrockgo.com/birthday?b=20230101&g=1'
# res = requests.get(url,timeout=3.0)
# res.raise_for_status()
# sleep(1)
d_list = []
while True:
    print(url)
    while True:
        res = requests.get(url,timeout=3.0)
        res.raise_for_status()
        sleep(2)
        soup = BeautifulSoup(res.content,'lxml')
        li_tags = soup.select('#birth_list > ul li')
        for li_tag in li_tags:
            div_tag = li_tag.select('div > div > div')[0]
            name_full_list = div_tag.select('p.main_name')
            name_full = name_full_list[0].text if name_full_list else ''
            name_jp_list = re.findall('[ぁ-ん]+[\s]*[ぁ-ん]*',div_tag.select_one('div').text)
            name_jp = name_jp_list[0] if name_jp_list else kata_to_hira(name_full)
            name_eng_list = div_tag.select('p.en_name')
            name_eng = name_eng_list[0].text if name_eng_list else ''
            title_list = re.findall('[ぁ-んァ-ン一-龥]+',div_tag.select_one('a').text)
            title = title_list[0] if title_list else ''
            title_eng_list = div_tag.select('a p')
            title_eng = title_eng_list[0].text if title_eng_list else ''
            print('='*10)
            print(name_jp)
            print(name_full)
            print(name_eng)
            print(title)
            print(title_eng)
            print('='*10)
            d_list.append({'読み方(ひらがな)':name_jp,
                           '正式名':name_full,
                           '英語表記':name_eng,
                           '作品名':title,
                           '作品名の英語表記':title_eng})
        a_tags = soup.select('a.page_next.hover')
        if a_tags:
            url = 'https://schara.sunrockgo.com/birthday' + a_tags[0].get('href')
        else:
            break
    if 'https://schara.sunrockgo.com/birthday?b=1231' in url:
        break
    next_page = soup.select('a[title="next Day"]')
    url = 'https://schara.sunrockgo.com/birthday' + next_page[0].get('href') + '&g=1'
df = pd.DataFrame(d_list)
df.to_excel('./mens_info.xlsx',index=False,encoding='utf-8')