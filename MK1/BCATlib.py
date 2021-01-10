from binance.client import Client
import json
from colorama import init, Fore, Back, Style
from time import sleep
import time
from binance.enums import *
init()
# klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

with open('config.json') as f:
  data = json.load(f)
client = Client(data["api_key"], data["api_secret"])
class Misc:
    def __init__(self, currency):
        self.currency = currency

    def current_price(currency):
        actual_price = client.get_avg_price(symbol=currency)
        print(f'{currency} is actually {Fore.YELLOW}{actual_price["price"]}{Style.RESET_ALL}')
        return actual_price["price"]

    def check_order_status(currency):
        actual_orders = client.get_open_orders()

        actual_orders = str(actual_orders)
        pos1 = actual_orders.find("orderId': ")
        pos2 = actual_orders.find(", 'orderListId")
        actual_orders = actual_orders[pos1:pos2]
        actual_orders = actual_orders.replace("orderId': ","")

        print(actual_orders)
        while True:
            if currency in actual_orders:
                print(f"Order {actual_orders} already placed.")
                time.sleep(2)
            else:
                print(f"Order placed with {actual_orders} ORDER UID")
       
        
class Trade:
    def __init__(self, currency, qty, price ):
        self.currency = currency
        self.price = price
    def buy(currency, qty, price):
        try:
            order = client.create_order(
                                        symbol=currency,
                                        side=SIDE_BUY,
                                        type=ORDER_TYPE_LIMIT,
                                        timeInForce=TIME_IN_FORCE_GTC,
                                        quantity=qty,
                                        price=price)
        except :
            print("Error on BUY ORDER")
        
    def sell():
        pass


class DataStore:
    def __init__(self, currency):
        self.currency = currency



       
    # def do_order():
    #     pass