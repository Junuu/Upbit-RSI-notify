import requests
import pandas as pd
import time
import pyupbit
import telegram
import datetime
import numpy as np


wait_dict = {}
tickers = pyupbit.get_tickers(fiat="KRW")

while True:    
    def rsiindex(symbol):
        url = "https://api.upbit.com/v1/candles/minutes/3"

        querystring = {"market":symbol,"count":"500"}

        response = requests.request("GET", url, params=querystring)

        data = response.json()
    
        df = pd.DataFrame(data)
    
        df=df.reindex(index=df.index[::-1]).reset_index()
    
        df['close']=df["trade_price"]
        
        
    
        def rsi(ohlc: pd.DataFrame, period: int = 14):
            ohlc["close"] = ohlc["close"]
            delta = ohlc["close"].diff()
    
            up, down = delta.copy(), delta.copy()
            up[up < 0] = 0
            down[down > 0] = 0
    
            _gain = up.ewm(com=(period - 1), min_periods=period).mean()
            _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
    
            RS = _gain / _loss
            return pd.Series(100 - (100 / (1 + RS)), name="RSI")
    
        rsi = rsi(df, 14).iloc[-1]
        print(symbol)
        print('Upbit 3 minute RSI:', rsi)
        
        
        btc_chat_id = 'your_chat_id'
        
        bot = telegram.Bot(token='yourToken')
        global wait_dict
        if rsi <= 25 and symbol not in wait_dict:            
            text = "RSI " + str(round(rsi)) + " : " + str(ticker)
            bot.sendMessage(chat_id=chat_id, text=text)
            wait_dict[symbol] = datetime.datetime.now().minute
        if rsi >= 70 and symbol not in wait_dict and symbol =="KRW-BTC":  
            text = "비트코인 상승 RSI 70 이상"
            bot.sendMessage(chat_id=btc_chat_id, text=text)
            wait_dict[symbol] = datetime.datetime.now().minute
        if rsi <= 30 and symbol not in wait_dict and symbol =="KRW-BTC":  
            text = "비트코인 상승 RSI 30 이하"
            bot.sendMessage(chat_id=btc_chat_id, text=text)
            wait_dict[symbol] = datetime.datetime.now().minute        
        print('')
        
        temp_dict = {}
        for key, value in wait_dict.items():
            if datetime.datetime.now().minute >= value:
                if datetime.datetime.now().minute - value < 5:
                    temp_dict[key] = value
            else:
                if datetime.datetime.now().minute + 60 -  value < 5:
                    temp_dict[key] = value
        wait_dict = temp_dict
        
        time.sleep(0.1)
           
       
    
    for ticker in tickers:
        try:
            rsiindex(ticker)
            
        except:
            print("error")
            continue
