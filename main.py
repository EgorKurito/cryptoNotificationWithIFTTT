import requests
import time
from datetime import datetime

YOYOW_API_URL = 'https://api.coinmarketcap.com/v1/ticker/yoyow/'
IFTTT_WEBHOOK_URL = 'https://maker.ifttt.com/trigger/{}/with/key/362PmcyA59FiWcnja7Bd9'
YOYOW_PRICE_THRESHOLD = 0.1

def get_latest_yoyow_price():
    response = requests.get(YOYOW_API_URL)
    response_json = response.json()
    return float(response_json[0]['price_usd'])

def post_ifttt_webhook(event, value):
    data = {'value1': value}
    ifttt_event_url = IFTTT_WEBHOOK_URL.format(event)
    requests.post(ifttt_event_url, json=data)

def format_yoyow_history(yoyow_history):
    rows = []
    for yoyow_price in yoyow_history:
        date = yoyow_price ['date'].strftime('%d.%m.%Y %H:%M')
        price = yoyow_price['price']
        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)
    return '<br>'.join(rows)

def main():
    yoyow_history = []
    while True:
        price = get_latest_yoyow_price()
        date = datetime.now()
        yoyow_history.append({'date': date, 'price': price})

        if price < YOYOW_PRICE_THRESHOLD:
            post_ifttt_webhook('price_emergency', price)

        if len(yoyow_history) == 5:
            post_ifttt_webhook('price_update', format_yoyow_history(yoyow_history))
            yoyow_history = []

        time.sleep(5)

if __name__ == '__main__':
    main()
