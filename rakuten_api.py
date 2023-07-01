import requests
import pandas as pd
import os
import sys

url = 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628'

# urlのパラメータ
params = {
    # 前手順で取得したアプリIDを設定する
    'applicationId':''
}

# APIを実行して結果を取得する
res = requests.get(url, params=params)

# JSONにデコードする
res_json = res.json()

# リスト作成
d_list = []

# ・順位
# ・店舗名
# ・URL
# ・ランキングのカテゴリ
with open('./楽天.txt', mode='w') as f:
    f.write(str(res_json))

for i in range(3):
    item = res_json['Items'][i]['Item']
    rank = item["rank"]
    shopName = item['shopName']
    itemUrl = item['itemUrl']
    title = res_json['title']

    d_list.append({'順位':rank,
                   '店舗名':shopName,
                   '商品url':itemUrl,
                   'カテゴリ':title})

filename = f"楽天.csv"

# csvファイルの出力先ディレクトリをappファイルの場所に設定
if getattr(sys, 'frozen', False):
    # frozen
    basedir = os.path.dirname(sys.executable)
else:
    # unfrozen
    basedir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(basedir, filename)

df = pd.DataFrame(d_list)
df.to_csv(file_path, index=False, encoding='utf-8-sig')