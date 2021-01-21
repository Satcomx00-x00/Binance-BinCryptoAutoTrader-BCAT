import json
import os
import time
from time import sleep
from datetime import datetime

from binance.client import Client
from binance.enums import *
from colorama import Back, Fore, Style, init
from prettytable import PrettyTable
from binance.websockets import BinanceSocketManager
from binance.enums import *

x = PrettyTable()
os.system('cls')

init()


with open('config.json') as f:
  data = json.load(f)
client = Client(data["api_key"], data["api_secret"])
###################################################################################################

###################################################################################################
def wallet_loader():
    futures_wallet=client.futures_account_balance()
    print(futures_wallet)
    BTC_balance = futures_wallet['BTC_balance']
    x.field_names = ["Curency", "Free", "Locked"]
    x.add_rows(
        [
            ["BTC", Fore.GREEN+BTC_balance['balance']+Style.RESET_ALL, Fore.YELLOW+BTC_balance['locked']+Style.RESET_ALL],
        ]
    )
    print(x)

def get_crypto_conf():
  with open('config.json') as f:
    config = json.load(f)

def data_stream():
    try:
        bm = BinanceSocketManager(client, user_timeout=5)
        conn_key = bm.start_kline_socket('BNBBTC', process_message, interval=KLINE_INTERVAL_30MINUTE)   

    #     # start any sockets here, i.e a trade socket
    #     conn_key = bm.start_trade_socket('BNBBTC', process_message)
    #     # then start the socket manager
    #     bm.start()
    except KeyboardInterrupt: 
        print("Keyboard Interrupt Exception")

def process_message(msg):
    if msg['e'] == 'error':
        # close and restart the socket
        print("Error")
        exit(1)
    else :
        print("message type: {}".format(msg['e']))
        print(msg)
    # do something

def main():
    os.system('cls')
    actual_time = datetime.now()
    print(f"Program start timestamp : {actual_time}")
    wallet_loader()
    data_stream()
    # avg_price = client.get_avg_price(symbol='BNBBTC')

if __name__ == "__main__":
    main()
    # cd C:\Users\rasps\Desktop\DEV\BINANCE-BOT\Binance-BinCryptoAutoTrader-BCAT\MK1\