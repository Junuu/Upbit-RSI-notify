# Upbit-RSI-notify
업비트 API와 텔레그램봇을 사용하여 일정시간마다 RSI가 일정 임계값을 넘거나 낮아지면 알림이 가는 서비스

## 실제 서비스 되고 있는 링크
https://t.me/cryptorsinotify


## 사용법
당신의 telegram bot의 토큰을 입력하세요
```
        bot = telegram.Bot(token='yourToken')
```
당신의 telegram 채팅방 id를 입력하세요
```
        btc_chat_id = 'your_chat_id'
```
세부 메시지를 변경하거나 알림받고 싶은 RSI강도를 조절할 수 있습니다.

현재는 symbol =="KRW-BTC"으로 설정되어있기 때문에 BTC에 대한 알림만 전송하게 됩니다. 

해당 부분을 제거하면 모든 암호화폐에 대한 알림을 받을 수 있습니다.
```
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
```
무분별한 메시지 전송을 막기위해 5분 텀을 두기위해서 작성한 코드입니다.

해당식을 적절하게 조절하여 사용할 수 있습니다.

1시 58분과 2시3분텀을 구분하기 위하여 현재시간이 가지고있는값보다 큰지 작은지를 확인하는 첫번째 분기를 가집니다.

만약 메시지 전송이 된지 5분이 지났다면 temp_dict[key]에 value가 입력되지 않을 것이며 비어있는 wait_dict를 가지게 됩니다.

```
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
```
