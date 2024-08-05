import requests
from bs4 import BeautifulSoup

# Yahoo天気APIのURL
YAHOO_WEATHER_URL = "https://weather.yahoo.co.jp/weather/jp/13/4410/13115.html"

# LINE Notifyの設定
LINE_NOTIFY_API = "https://notify-api.line.me/api/notify"
LINE_NOTIFY_TOKEN = "9CGCZY58c9hsPsaOG0Qyp5wltwnlMkS6mf7bN1wzNAl"

def get_weather():
    response = requests.get(YAHOO_WEATHER_URL)
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

def send_line_notify(message):
    headers = {
        "Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"
    }
    data = {
        "message": message
    }
    requests.post(LINE_NOTIFY_API, headers=headers, data=data)

if __name__ == "__main__":
    weather_message = get_weather()
    if weather_message:
        send_line_notify(weather_message)
