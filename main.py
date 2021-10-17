import requests
from twilio.rest import Client

twilio_acc = "your account sid"
auth_token = "your auth token"


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla inc."

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_ENDPOINT= "https://www.alphavantage.co/query?"

STOCK_API = "ypur stock api"
NEWS_API = "your news api"
params ={
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API,
}

response = requests.get(STOCK_ENDPOINT,params=params)
stock_data = response.json()
stock_slice = stock_data["Time Series (Daily)"]

data_list = [value for (key,value) in stock_slice.items()]
yesterday_data = data_list[0]
dates=[]
for key in stock_slice:
    dates.append(key)

yesterday_closing_price = yesterday_data["4. close"]

yesterday_data = data_list[1]
day_before_closing_price = yesterday_data["4. close"]

difference = (float(yesterday_closing_price)-float(day_before_closing_price))
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_perc = round((difference/float(yesterday_closing_price)) * 100)

if abs(diff_perc) > 1:
    news_params ={
        "apiKey": NEWS_API,
        "qInTitle": COMPANY_NAME
    }
    data = requests.get(NEWS_ENDPOINT,params=news_params)
    articles = data.json()["articles"]
    two_articles = articles[:3]
    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_perc}%\n {dates[0]}:${round(float(yesterday_closing_price),3)}\n{dates[1]}:${round(float(day_before_closing_price),3)}\n Headline: {article['title']}\n Brief: {article['description']}" for article in two_articles]

    client = Client(twilio_acc, auth_token)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="twilio number",
            to= "your number"
        )
