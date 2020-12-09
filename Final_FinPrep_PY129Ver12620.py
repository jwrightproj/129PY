# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 08:44:35 2020

@author: JWRIGHT

This program retrieves information from an financial info from the
Financial Prep API and writes out comma delimited file
that will be take in by program DATABASE FINAL 1129_SBMT.py
"""
import requests,json
import pandas as pd
#*************************************************
#Choose Stock Gainers
#*************************************************
resp = requests.get("https://financialmodelingprep.com/api/v3/gainers?apikey=5507ab7b5ed87b9fd6be726094362361")
print('***Executed request1')
resp.json()
#import pandas as pd
pd.set_option('display.max_columns', None)
msgs = pd.io.json.json_normalize(resp.json())
msgs.dtypes
print(msgs.dtypes)
df2 = pd.DataFrame({'changesPercentage': msgs.changesPercentage.head(100),
                    'changes': msgs.changes.head(100),
                    'ticker': msgs.ticker.head(100),
                   'companyName': msgs.companyName.head(100)})
for i, row in df2.iterrows():
    comp=row['companyName']
    print('Company Name',comp)
    tckr = row['ticker']
    print('Ticker',tckr)
    ChangePer = row['changesPercentage']
    print('Change in Percentage',ChangePer)
    change = row['changes']
    print('Change',change)
    print(' ')
    print('********************************')
"""

"""
#****************************************************
#Web scrap with pulling the recent articles on any valid stock and listing in dataframe
#****************************************************
 
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt

tickersym=input('Enter a gainer to get information:')

finviz_url = 'https://finviz.com/quote.ashx?t='

tickers =  ["'" + tickersym + "'"]

news_arts = {}
for ticker in tickers:
    url = finviz_url + ticker

    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)

    html = BeautifulSoup(response, features='html.parser')
    news_tab = html.find(id='news-table')
    news_arts[ticker] = news_table
    
parsed_data = []

for ticker, news_tab in news_arts.items():
    for row in news_tab.findAll('tr'):
        title = row.a.text
        date_data = row.td.text.split(' ')

        if len(date_data) == 1:
            time = date_data[0]
        else:
            date = date_data[0]
            time = date_data[1]

        parsed_data.append([ticker, date, time, title])

df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])
df['date'] = pd.to_datetime(df.date).dt.date
from IPython.display import HTML
print(df)                 

#**************************************************
#Do a company profile request from financial model prep and write to csv
#*************************************************
resp = requests.get("https://financialmodelingprep.com/api/v3/profile/AAPL?apikey=5507ab7b5ed87b9fd6be726094362361")
print('***Executed request')
#resp.raise_for_status()
resp.json()
#import pandas as pd
msgs = pd.io.json.json_normalize(resp.json())
msgs.dtypes
df = pd.DataFrame({'Company': msgs.companyName.head(100),
                   'CEO': msgs.ceo.head(100),
                   'Industry': msgs.industry.head(100),
                   'Desc': msgs.description.head(100),
                   'symbol': msgs.symbol.head(100)})
print(df)
print('******printing to company csv')
df.to_csv('companyinfo.csv', sep=',', encoding='utf-8')
#*************************************************
#Do a stock news profile request from financial model prep to csv
#*************************************************
resp = requests.get("https://financialmodelingprep.com/api/v3/stock_news?tickers=AAPL&limit=50&apikey=5507ab7b5ed87b9fd6be726094362361")
#resp.raise_for_status()
print('Executed Request')
resp.json()[0]
#import pandas as pd
msgs2 = pd.io.json.json_normalize(resp.json())
print(msgs2.dtypes)
df3 = pd.DataFrame({
                   'symbol': msgs2.symbol.head(100),
                   'text':   msgs2.text.head(100),
                   'urlinfo': msgs2.url.head(100)})
print(df3)
print('******printing to stock csv')
df3.to_csv('stockinfo.csv', sep=',', encoding='utf-8')
#****************************************************