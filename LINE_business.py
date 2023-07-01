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
import openpyxl

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--user-agent=  Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36')

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

url = 'https://account.line.biz/login?redirectUri=https%3A%2F%2Fmanager.line.biz%2Finvitation%2FR8Y21PYgNpY9glP8D6FDjZq4IIjU95'

driver.get(url)
sec = random.uniform(5,10)
sleep(sec)
driver.implicitly_wait(30)

box = driver.find_element(By.CSS_SELECTOR,'div.px-3.mb-4 > a')
box.click()
sleep(sec)

bars = driver.find_elements(By.CSS_SELECTOR,'div> input')

# エクセルファイルのパス
excel_file_path = "./input情報.xlsx"

# エクセルファイルの読み込み
workbook = openpyxl.load_workbook(excel_file_path)

# シート名を指定
sheet_name = "シート1"
sheet = workbook[sheet_name]

# B列の値を読み込んで変数に代入
mailadress = sheet["B2"].value
keyword = sheet["B3"].value
message = sheet["B4"].value

bars[1].send_keys(mailadress)
sleep(sec)
bars[2].send_keys(keyword)
sleep(sec)

Login_button = driver.find_element(By.CSS_SELECTOR,' div:nth-of-type(4) > button')
Login_button.click()
sleep(sec)

d_list = []

while True:
    list_button = driver.find_elements(By.CSS_SELECTOR,'#contents > div > div > div > div > button')
    if list_button:
        list_button[0].click()
        sleep(sec)
    # TODO
    # boxes = driver.find_elements(By.CSS_SELECTOR,'td > a > div')
    names = driver.find_elements(By.CSS_SELECTOR,' a > div > div:nth-of-type(2)')
    name = names[-1].text
    print(name)
    for i in range(len(names)):
        boxes = driver.find_elements(By.CSS_SELECTOR,'td > a > div')
        box = boxes[i]
        print(box.text)
        box.click()
        sleep(sec)
        close =  driver.find_elements(By.CSS_SELECTOR,'.modal-header.flex-shrink-0 > button > i')
        if close:
            close[0].click()
            sleep(sec)
        chat_page = driver.find_elements(By.CSS_SELECTOR,'li:nth-of-type(8) > a')

        if chat_page:
            chat_page[0].click()
            sleep(sec)
            # 別のウィンドウまたはタブに切り替える
            driver.switch_to.window(driver.window_handles[-1])
            sleep(sec)
            close2 = driver.find_elements(By.CSS_SELECTOR,'div.modal-header.flex-shrink-0 > button')
            if close2:
                close2[0].click()
                sleep(sec)

            # スクロールする要素を取得
            scrollable_elements = driver.find_elements(By.CSS_SELECTOR, 'div.chatlist.d-flex.flex-column.justify-content-center.flex-fill.h-min-0 > div.flex-fill.overflow-y-auto')
            if scrollable_elements:
                # スクロールする高さを取得
                scroll_height = scrollable_elements[0].get_attribute('scrollHeight')

                # スクロールが完了するまで待機
                while True:
                    # スクロール実行
                    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight;', scrollable_elements[0])
                    current_scroll_height = driver.execute_script('return arguments[0].scrollTop;', scrollable_elements[0])
                    print(current_scroll_height)
                    if current_scroll_height == scroll_height:
                        print('スクロールが完了しました')
                        break
                    scroll_height = current_scroll_height
                    print(scroll_height)
                sleep(sec)

            friend_boxes = driver.find_elements(By.CSS_SELECTOR,'div.flex-fill.overflow-y-auto > div > div > a')
            print(len(friend_boxes))
            for friend_box in friend_boxes:
                friend_name_tag = friend_box.find_element(By.CSS_SELECTOR,' div.d-flex.align-items-center.mb-1 > h6')
                friend_name = friend_name_tag.text
                friend_box.click()
                sleep(5)
                message_box = driver.find_elements(By.CSS_SELECTOR,'#editor > textarea')
                if message_box:
                    try:
                        message_box[0].send_keys(message)
                        sleep(sec)
                        # リターンキーを押す
                        message_box[0].send_keys(Keys.RETURN)
                        # エンターキーを押す
                        # message_box[0].send_keys(Keys.ENTER)
                        now = datetime.datetime.now()
                        formatted_datetime = now.strftime("%Y/%m/%d %H:%M:%S")
                        d_list.append({
                                    '対象者名':friend_name,
                                    '送信日時':formatted_datetime,
                                    '文言':message
                                    })
                        sleep(sec)
                    except:
                        pass
            if friend_boxes:
                driver.close()
                sleep(sec)
            else:
                close3 = driver.find_elements(By.CSS_SELECTOR,'div.modal-header.flex-shrink-0 > button')
                if close3:
                    close3[0].click()
                    sleep(sec)
            # 元のページに切り替える
            driver.switch_to.window(driver.window_handles[0])
        driver.back()
        sleep(sec)
    next_page = driver.find_element(By.CSS_SELECTOR,' nav > ul > li:last-of-type')
    next_page.click()
    sleep(sec)
    last_names = driver.find_elements(By.CSS_SELECTOR,' a > div > div:nth-of-type(2)')
    last_name = last_names[-1].text
    # print(last_name)
    if name == last_name:
        break

try:
    driver.quit()
except:
    pass
now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
filename = f"log_{now}.csv"


if getattr(sys, 'frozen', False):
    basedir = os.path.dirname(sys.executable)
else:
    basedir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(basedir, filename)

df = pd.DataFrame(d_list)
df.to_csv(file_path,index=False,encoding='utf-8-sig')
print('動作が終了しました。')