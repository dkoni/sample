import instaloader

# インスタンスを作成
loader = instaloader.Instaloader()

your_username = 'basuozi015'
your_password = 'GYRN?L-rUt29+3L'

# ログイン
loader.login(your_username, your_password)

# セッション保存
loader.save_session_to_file("session")

# URLリストを読み込む
with open("url_list.rtf", "r") as f:
    url_list = f.readlines()

url_list = ['https://www.instagram.com/watanabenaomi703/','https://www.instagram.com/ksm_ksm21/']
print(url_list)
# オープンアカウントと鍵アカウントに分ける
open_accounts = []
private_accounts = []

for url in url_list:
    # URLからユーザー名を抽出
    username = url.strip().split("/")[-2]

    try:
        # ユーザープロファイルを取得
        profile = instaloader.Profile.from_username(loader.context, username)

        # プロファイルのis_private属性を確認して分類する
        if profile.is_private:
            private_accounts.append(url.strip())
        else:
            open_accounts.append(url.strip())

    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Invalid URL or username not found: {url.strip()}")

# オープンアカウントと鍵アカウントを出力
print("Open accounts:")
print(open_accounts)
print("Private accounts:")
print(private_accounts)
