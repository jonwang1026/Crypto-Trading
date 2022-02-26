import pandas as pd
from time import sleep
import sqlalchemy
from binance.client import Client
from binance import BinanceSocketManager
from info import *


def createFrame(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:, ['s', 'E', 'p']]
    df.columns = ['symbol', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')
    return df


def getCurrData(msg):
    while True:
        sleep(5)
        await socket.__aenter__()
        msg = await socket.recv()
        frame = createFrame(msg)
        frame.to_sql(pair, engine, if_exists='append', index=False)
        print(frame)

#  trading strategy


def strategy(entry, lookback, qty, open_position=False):
    while True:
        df = pd.read_sql(pair, engine)
        lookbackperiod = df.iloc[-lookback:]
        cumret = (lookbackperiod.Price.pct_change() + 1).cumprod() - 1
        if not open_position:
            if cumret[cumret.last_valid_index()] > entry:
                order = client.create_order(symbol=pair,
                                            side='BUY',
                                            type='MARKET',
                                            quantity=qty)
                print(order)
                open_position = True
                break
    if open_position:
        while True:
            df = pd.read_sql('BTCUSDT', engine)
            sincebuy = df.loc[df.Time >
                              pd.to_datetime(order['transactTime'],
                                             unit='ms')]
            if len(sincebuy) > 1:
                sincebuyret = (sincebuy.Price.pct_change() + 1).cumprod() - 1
                last_entry = sincebuyret[sincebuyret.last_valid_index()]
                if (last_entry > 0.0015) or (last_entry < -0.0015):
                    order = client.create_order(symbol=pair, side='SELL', type='MARKET', quantity=qty)
                    print(order)
                    break


if __name__ == "__main__":
    # add in your api_keys and api secret from website
    client = Client(api_key, api_secret)
    engine = sqlalchemy.create_engine('sqlite:///stream.db')
    bsm = BinanceSocketManager(client)
    socket = bsm.trade_socket(pair)
    strategy(0.001, 60, 0.001)
