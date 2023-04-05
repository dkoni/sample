import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import re

url ='https://imitsu.jp/ct-hp-design/bu-lpo-company/?transition=global_menu&pn=1#title'
headers = {
    'User_Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }

kennsyo = 1
index_num = 1
d_list = []
while True:
    res = requests.get(url, headers=headers, timeout=3.0)
    res.raise_for_status()
    sleep(1)

    soup = BeautifulSoup(res.content,'lxml')

    site_name = 'アイミツ'
    category = 'LPOに強いホームページ制作会社一覧'
    page = ''.join(filter(str.isdigit, url))
    boxes = soup.select('div.list-box > article')
    for box in boxes:
        company = box.select('h3>a')[0].text
        page_url = box.select('h3>a')[0].get('href')

        try:
            page_res = requests.get(page_url,headers=headers,timeout=3.0)
            page_res.raise_for_status()
            sleep(1)
            page_soup = BeautifulSoup(page_res.content,'lxml')

            post_start_year = page_soup.select('div > dl:contains("設立年") > dd')
            if post_start_year:
                start_year = post_start_year[0].text
            else:
                start_year = ''
            post_company_people = page_soup.select('div > dl:-soup-contains("社員数") > dd')
            if post_company_people:
                company_people = post_company_people[0].text
            else:
                company_people=''
            post_min_order = page_soup.select('div > dl:-soup-contains("最低受注金額") > dd')
            if post_min_order:
                min_order = post_min_order[0].text
            else:
                min_order=''
            post_achievement = page_soup.select('div > dl:-soup-contains("実績数") > dd')
            if post_achievement:
                achievement = post_achievement[0].text
            else:
                achievement = ''
            post_employee = page_soup.select('div > dl:-soup-contains("従業員数") > dd')
            if post_employee:
                employee = post_employee[0].text
            else:
                employee = ''

            post_text = page_soup.select('section.surrounding-city-list-sec > h2')
            if post_text:
                text = post_text[0].text
                region = re.findall('(.+?[都道府県])',text)[0]
            else:
                region = ''
            post_cost = page_soup.select('div > dl:-soup-contains("予算") > dd')
            if post_cost:
                cost = post_cost[0].text
            else:
                cost = ''
            post_HP_url = page_soup.select('div > dl:-soup-contains("会社URL") > dd')
            if post_HP_url:
                HP_url = post_HP_url[0].text
            else:
                HP_url = ''
            d_list.append({'NO':index_num,
                        'サイト':site_name,
                        'カテゴリー':category,
                        'ページ数':page,
                        '会社名':company,
                        'HPURL':HP_url,
                        '創業年数':start_year,
                        '社員数':company_people,
                        '最低受注金額':min_order,
                        '実績数':achievement,
                        '従業員数':employee,
                        '地域':region,
                        '予算':cost,
                        'ページURL':page_url})
        except requests.exceptions.HTTPError:
            print('HTTPが不正です')
            pass
    index_num += 1
    next = soup.select('nav > ul > li > a[rel="next"]')
    print(f'{kennsyo}回目')
    kennsyo += 1
    if next:
        url = next[0].get('href')
    else:
        break
df = pd.DataFrame(d_list)
df.to_excel('./競合リサーチ.xlsx',index=False,encoding='utf-8-sig')