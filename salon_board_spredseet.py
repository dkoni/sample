from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd
import datetime
import os
import sys
import re
import random
from oauth2client.service_account import ServiceAccountCredentials
import gspread


options = webdriver.ChromeOptions()

options.add_argument("--proxy-server=")
options.add_argument('--user-agent=  Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36')


driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


url = 'https://salonboard.com/login/'

# ------------------------------------------------------------- Google APIの設定 -----------------------------------------------------------------------------------
# Google APIにアクセス
scope =['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('', scope)
client = gspread.authorize(creds)
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
#スプレッドシートIDを変数に格納する。
SPREADSHEET_KEY = ''
# スプレッドシート（ブック）を開く
workbook = client.open_by_key(SPREADSHEET_KEY)

# シートの一覧を取得する。（リスト形式）
worksheets = workbook.worksheets()

# シートを開く
worksheet = workbook.get_worksheet(0)

# パスワードを取得
ID_list = worksheet.range('A2:A1000')
password_list = worksheet.range('B2:B1000')

print(ID_list[0].value)
print(password_list[0].value)


for i in range(len(ID_list)):
    if ID_list[i].value != '':
        d_list = []
        driver.get(url)
        sec = random.uniform(5,10)
        sleep(sec)
        driver.implicitly_wait(10)

        ID_box = driver.find_element(By.CSS_SELECTOR,'dl > dd > input')
        Pass_box = driver.find_element(By.CSS_SELECTOR,'input.loginPwInput')
        login = driver.find_element(By.CSS_SELECTOR,'#idPasswordInputForm > div > div.columnBlock.mt46.ml15 > a')


        ID_box.send_keys(ID_list[i].value)
        sleep(sec)
        Pass_box.send_keys(password_list[i].value)
        sleep(sec)


        login.click()
        sleep(sec)


        name_tag = driver.find_element(By.CSS_SELECTOR,'ul.shop_name_wrap > li.shop_login_name')
        name = name_tag.text


        analysis_tab = driver.find_elements(By.CSS_SELECTOR,'#globalNavi > ul.btn01.cf > li:nth-of-type(6) > a > img')
        if analysis_tab:
            analysis_tab[0].click()
            sleep(sec)

        daily_sales = driver.find_elements(By.CSS_SELECTOR,'#jsiSideBar > dd:nth-of-type(1) > ul > li:nth-of-type(1) > a')
        daily_sales[0].click()
        sleep(sec)

        date_tags = driver.find_elements(By.CSS_SELECTOR,'#dailySalesContents > div.rightContents.oh > div.mt10 > table > tbody > tr> th.smallArticle.searchDateCell')
        net_sales = driver.find_elements(By.CSS_SELECTOR,'#dailySalesContents > div.rightContents.oh > div.mt10 > table > tbody > tr > td:nth-of-type(1)')
        medicals = driver.find_elements(By.CSS_SELECTOR,'#dailySalesContents > div.rightContents.oh > div.mt10 > table > tbody > tr > td:nth-of-type(2)')
        stores = driver.find_elements(By.CSS_SELECTOR,'#dailySalesContents > div.rightContents.oh > div.mt10 > table > tbody > tr > td:nth-of-type(3)')
        options = driver.find_elements(By.CSS_SELECTOR,'#dailySalesContents > div.rightContents.oh > div.mt10 > table > tbody > tr > td:nth-of-type(4)')
        totals = driver.find_elements(By.CSS_SELECTOR,'#dailySalesContents > div.rightContents.oh > div.mt10 > table > tbody > tr > td:nth-of-type(5)')
        discounts = driver.find_elements(By.CSS_SELECTOR,'#dailySalesContents > div.rightContents.oh > div.mt10 > table > tbody > tr > td:nth-of-type(6)')
        customer_incomes = driver.find_elements(By.CSS_SELECTOR,'#dailySalesContents > div.rightContents.oh > div.mt10 > table > tbody > tr > td:nth-of-type(7)')
        customers = driver.find_elements(By.CSS_SELECTOR,'#dailySalesContents > div.rightContents.oh > div.mt10 > table > tbody > tr > td:nth-of-type(8)')
        news = driver.find_elements(By.CSS_SELECTOR,'#dailySalesContents > div.rightContents.oh > div.mt10 > table > tbody > tr > td:nth-of-type(9)')
        ageins = driver.find_elements(By.CSS_SELECTOR,'#dailySalesContents > div.rightContents.oh > div.mt10 > table > tbody > tr > td:nth-of-type(10)')
        nominations = driver.find_elements(By.CSS_SELECTOR,'#dailySalesContents > div.rightContents.oh > div.mt10 > table > tbody > tr > td:nth-of-type(11)')
        medicals_2 = driver.find_elements(By.CSS_SELECTOR,'#dailySalesContents > div.rightContents.oh > div.mt10 > table > tbody > tr > td:nth-of-type(12)')
        stores_2 = driver.find_elements(By.CSS_SELECTOR,'#dailySalesContents > div.rightContents.oh > div.mt10 > table > tbody > tr > td:nth-of-type(13)')
        options_2 = driver.find_elements(By.CSS_SELECTOR,'#dailySalesContents > div.rightContents.oh > div.mt10 > table > tbody > tr > td:nth-of-type(14)')
        discounts_2 = driver.find_elements(By.CSS_SELECTOR,'#dailySalesContents > div.rightContents.oh > div.mt10 > table > tbody > tr > td:nth-of-type(15)')
        persons = driver.find_elements(By.CSS_SELECTOR,'#dailySalesContents > div.rightContents.oh > div.mt10 > table > tbody > tr > td:nth-of-type(16)')
        totals_total = driver.find_element(By.CSS_SELECTOR,'#dailySalesContents > div.rightContents.oh > div.mt10 > table > tbody > tr.bdrT2 > td:nth-of-type(2)')

driver.quit()
