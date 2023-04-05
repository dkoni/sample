import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--user-agent==Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')

url = 'https://www.mizuhobank.co.jp/retail/takarakuji/check/numbers/backnumber/index.html'
driver = webdriver.Chrome(options=options)
driver.get(url)
driver.implicitly_wait(10)
sleep(3)
soup = BeautifulSoup(driver.page_source,'lxml',from_encoding='utf-8')
driver.quit()

tbody_tag = soup.select_one('div > table.typeTK.js-backnumber-b > tbody')
a_tags = tbody_tag.select('tr > td > a')

headers = {
    'User_Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }

round_nums = []
dates = []
nums3 = []
nums4 = []

for a_tag in a_tags:
    if a_tag.get('href') == '':
        break
    base_url = 'https://www.mizuhobank.co.jp'+ a_tag.get('href')
    if 'detail.html?' in base_url :
        driver = webdriver.Chrome(options=options)
        driver.get(base_url)
        sleep(3)
        page_soup = BeautifulSoup(driver.page_source,'lxml')
        driver.quit()
    else:
        page_res = requests.get(base_url,headers=headers,timeout=3.0)
        page_res.raise_for_status()
        sleep(1)
        page_soup = BeautifulSoup(page_res.content,'lxml',from_encoding='utf-8')
    page_tbody_tags = page_soup.select('div.pc-none > table > tbody')
    for page_tbody_tag in page_tbody_tags:
        round_num = page_tbody_tag.select_one('tr:nth-of-type(1) > td').text
        date = page_tbody_tag.select_one('tr:nth-of-type(2) > td').text
        num3 = page_tbody_tag.select_one('tr:nth-of-type(3) > td').text
        num4 = page_tbody_tag.select_one('tr:nth-of-type(4) > td').text
        round_nums.append(round_num)
        dates.append(date)
        nums3.append(num3)
        nums4.append(num4)
    print(round_nums[-1])
df = pd.DataFrame({'回別':round_nums,
                   '抽選日':dates,
                   'ナンバー3抽選数字':nums3,
                   'ナンバー4抽選数字':nums4})
df.to_csv('./mizuho_lottery.csv',index=False,encoding='utf-8-sig')