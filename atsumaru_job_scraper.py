from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import requests
from bs4 import BeautifulSoup
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--user-agent==Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')

driver = webdriver.Chrome(options=options)
driver.get('https://atsumaru.jp/area/7/list?sagid=all')
driver.implicitly_wait(10)

new_height = 0
while True:
    height = driver.execute_script('return document.body.scrollHeight')
    driver.execute_script(f'window.scrollTo(0,{height})')
    sleep(3)
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == height:
        break

soup = BeautifulSoup(driver.page_source,'lxml')
sleep(1)
jobs = soup.select('h2.bl_card2_ttl span a')
len(jobs)
companys = []
addresses = []
tell_nums = []
for job in jobs:
    job_url = 'https://atsumaru.jp' + job.get('href')
    res = requests.get(job_url)
    sleep(1)
    post_soup = BeautifulSoup(res.content,'lxml')
    # 企業名
    try:
        company = post_soup.select_one('span.bl_card2_ttl_text').text
    except AttributeError:
        company = 'Not Found'
    # 住所
    tr_tags = post_soup.select('tr:-soup-contains("住所")')
    if tr_tags:
        address = tr_tags[0].select_one('td > p').text
    else:
        tr_tags = post_soup.select('tr:-soup-contains("勤務地")')
        if tr_tags:
            address = tr_tags[0].select_one('td > p').text
        else:
            address = 'Not Found'
    # 電話番号
    try:
        tells = post_soup.select('div.telNo > p >strong >a')
        if not tells:
            raise AttributeError
        tell_num = tells[-1].text
    except AttributeError:
        tells = post_soup.select('div.telNo')
        if not tells:
            tell_num = 'Not found'
        else:
            tell_num = tells[-1].text.split('／')[-1]
    companys.append(company)
    addresses.append(address)
    tell_nums.append(tell_num)

df = pd.DataFrame({'企業名':companys,
                   'アドレス':addresses,
                   '電話番号':tell_nums})
df.to_csv('./あつまるくんdate.csv',index=False,encoding='utf-8-sig')

print('動作終了')