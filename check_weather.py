import os
import requests
from bs4 import BeautifulSoup
import logging

# ログの設定
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Yahoo天気APIのURL
YAHOO_WEATHER_URL = "https://weather.yahoo.co.jp/weather/jp/13/4410/13115.html"

# LINE Notifyの設定
LINE_NOTIFY_API = "https://notify-api.line.me/api/notify"
LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")  # 環境変数から取得

# LINE Notifyトークンの確認
if not LINE_NOTIFY_TOKEN:
    logging.error("LINE_NOTIFY_TOKENが設定されていません。環境変数を確認してください。")
    raise ValueError("LINE_NOTIFY_TOKENが設定されていません。")

def get_weather():
    try:
        response = requests.get(YAHOO_WEATHER_URL)
        response.raise_for_status()  # HTTPエラーがあれば例外をスロー
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # <div id="yjw_pinpoint_today"> 内の <small> 要素を取得
        pinpoint_today_div = soup.find('div', id='yjw_pinpoint_today')
        if pinpoint_today_div:
            small_elements = pinpoint_today_div.find_all('small', text=True)
            
            # <small> 要素のテキストに「雨」や「曇り」が含まれているかをチェック
            for small in small_elements:
                text = small.get_text()
                if "雨" in text:
                    return "雨かも"
                elif "曇り" in text:
                    return "今日は曇りの予報です。"

        return None

    except requests.RequestException as e:
        logging.error(f'Weather APIからデータを取得中にエラーが発生しました: {e}')
        return None
    except Exception as e:
        logging.error(f'予期しないエラーが発生しました: {e}')
        return None

def send_line_notify(message):
    try:
        headers = {
            "Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"
        }
        data = {
            "message": message
        }
        response = requests.post(LINE_NOTIFY_API, headers=headers, data=data)
        response.raise_for_status()  # HTTPエラーがあれば例外をスロー
        logging.info(f'通知が送信されました: {message}')
    
    except requests.RequestException as e:
        logging.error(f'LINE Notifyに通知を送信中にエラーが発生しました: {e}')
    except Exception as e:
        logging.error(f'予期しないエラーが発生しました: {e}')

if __name__ == "__main__":
    weather_message = get_weather()
    if weather_message:
        send_line_notify(weather_message)
    else:
        logging.info('天気情報がありません。通知は送信されませんでした。')
