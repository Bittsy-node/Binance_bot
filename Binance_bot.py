import websocket, json, pprint, talib, numpy


# Connect to Binance Websocket
SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"

# Strategy Settings
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = BTCUSDT
TRADE_QUANTITY = 0.0001
MAX_POSITION = 0.0010
MIN_POSITION = -0.0010

# Create global variable for candle closing prices
closes = []

# Create position variable - AMEND TO READ FROM API
position = 0
 
def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    global closes

    json_message=json.loads(message)
    pprint.pprint(json_message)

    candle = json_message['k']
        
    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print("candle closed at {}".format(close))
        closes.append(float(close))
        print("closes")
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("calculated RSIs")
            print(rsi)
            last_rsi = rsi[-1]
            print("Current RSI {}".format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT:
                if position > MIN_POSITION:
                    print("Executing Sell")
                    # Trigger Sell
                else:
                    print("Maximum Position Reached")

            if last_rsi < RSI_OVERSOLD:
                print("Executing Buy")






    
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()

