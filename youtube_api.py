import google.auth
from googleapiclient.discovery import build
import re

# APIキーを取得
api_key = ''
api_key = ''

# YouTube Data APIのビルド
youtube = build('youtube', 'v3', developerKey=api_key)

# チャンネルIDを指定してチャンネル情報を取得する関数
def get_channel_info(channel_id):
    # channels().list()メソッドを使用してチャンネル情報を取得する
    response = youtube.channels().list(
        part='snippet, statistics',
        id=channel_id
    ).execute()

    # レスポンスから必要な情報を抽出する
    channel = response['items'][0]
    channel_name = channel['snippet']['title']
    channel_description = channel['snippet']['description']
    subscriber_count = channel['statistics']['subscriberCount']
    video_count = channel['statistics']['videoCount']
    last_updated = channel['snippet']['publishedAt']

    # チャンネルのメールアドレスを検索
    email = 'メールアドレスが見つかりませんでした。'
    try:
        about_response = youtube.channels().list(
            part='snippet',
            id=channel_id
        ).execute()
        about_text = about_response['items'][0]['snippet']['aboutChannel']['description']
        email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', about_text).group(0)
    except:
        pass

    # 結果を辞書形式で返す
    result = {
        'channel_name': channel_name,
        'channel_description': channel_description,
        'subscriber_count': subscriber_count,
        'video_count': video_count,
        'last_updated': last_updated,
        'email': email
    }
    return result

# サプーのチャンネルID
id = 'UC5Kgc_HNzx4GJ-w4QMeeKiQ'

sapu_id =  get_channel_info(id)

print(sapu_id)
