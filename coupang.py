import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import pandas as pd
import datetime
import os
import sys


class App:
    def __init__(self, master):
        self.master = master
        master.title("coupang")

        # GUI widgets
        self.url_label = tk.Label(master, text="URL: ")
        self.url_label.grid(row=1, column=0)

        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.grid(row=1, column=1)

        self.add_button = tk.Button(master, text="追加", command=self.add_url, width=8)
        self.add_button.grid(row=1, column=2)

        self.url_listbox = tk.Listbox(master, width=80)
        self.url_listbox.grid(row=2, columnspan=3)

        self.delete_button = tk.Button(master, text="削除", command=self.delete_url, width=8)
        self.delete_button.grid(row=3, column=0)

        self.delete_all_button = tk.Button(master, text="全削除", command=self.delete_all_urls, width=8)
        self.delete_all_button.grid(row=3, column=1)

        self.execute_button = tk.Button(master, text="実行", command=self.execute, width=8)
        self.execute_button.grid(row=3, column=2)


    def add_url(self):
        url = self.url_entry.get()

        if url.startswith("https://store.coupang.com/vp/vendors/"):
            self.url_listbox.insert(tk.END, url)
            self.url_entry.delete(0, tk.END)
        else:
            tk.messagebox.showerror("エラー", "有効なURLを入力してください。")

    def delete_url(self):
        try:
            selected_index = self.url_listbox.curselection()[0]
            self.url_listbox.delete(selected_index)
        except IndexError:
            pass

    def delete_all_urls(self):
        self.url_listbox.delete(0, tk.END)

    def execute(self):
        for url in self.url_listbox.get(0, tk.END):
            self.scrape_url(url)
        self.master.destroy()

    def scrape_url(self, url):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')

        d_list = []

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


        driver.get(url)
        driver.implicitly_wait(10)


        page_sort = driver.find_element(By.CSS_SELECTOR,'#sortingFilter > li.seller-page-sort-are__sort__sort-item')
        page_sort.click()
        sleep(5)

        new_height = 0
        while True:
            height = driver.execute_script('return document.body.scrollHeight')
            driver.execute_script(f'window.scrollTo(0,{height})')
            sleep(3)
            new_height = driver.execute_script('return document.body.scrollHeight')
            if new_height == height:
                break

        sleep(3)
        soup = BeautifulSoup(driver.page_source,'lxml')
        driver.quit()

        li_tags = soup.select('#product-list > li')

        for li_tag in li_tags:
            Product = li_tag.select('a')
            if Product:
                Product_URL = Product[0].get('href')
            else:
                Product_URL = 'Not found'
            cost = li_tag.select('a > dl > dd > div.product-price-area > em > strong')
            if cost:
                Product_cost = cost[0].text
            else:
                Product_cost = 'Not found'
            d_list.append({
                '出品者URL':url,
                '商品URL':Product_URL,
                '価格':Product_cost
            })


        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"coupang_{now}.csv"


        if getattr(sys, 'frozen', False):
            basedir = os.path.dirname(sys.executable)
        else:
            basedir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(basedir, filename)

        df = pd.DataFrame(d_list)
        df.to_csv(file_path,index=False,encoding='utf-8-sig')

        print(f'動作完了。ファイル {filename} に保存しました。')

    def show_help(self):
        help_window = tk.Toplevel(self.master)
        help_window.title("ヘルプ")

        message = "・追加ボタン: 入力欄に入力されたURLをリストに追加する\n\n" \
                "・削除ボタン: リスト内で現在選択されているURLを削除する\n\n" \
                "・全削除ボタン: リスト内の全てのURLを削除する\n\n" \
                "・実行ボタン: リスト内の全てのURLをスクレイピングする\n\n"

        message_label = tk.Label(help_window, text=message, justify="left")
        message_label.pack()


root = tk.Tk()
app = App(root)
root.mainloop()