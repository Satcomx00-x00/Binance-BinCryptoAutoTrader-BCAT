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

    def current_price(self, currency):
        actual_price = client.get_avg_price(symbol=currency)
        print(f'{currency} is actually {Fore.YELLOW}{actual_price["price"]}{Style.RESET_ALL}')
        return actual_price["price"]

    def check_order_status(self, currency):
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

class Method :
    def __init__(self, currency):
        self.currency = currency
    

    def grid_gamble(self, currency):
        def current_price(self, currency):
            actual_price = client.get_avg_price(symbol=currency)
            print(f'{currency} is actually {Fore.YELLOW}{actual_price["price"]}{Style.RESET_ALL}')
            # actual_price = actual_price["price"].replace(".",",")
            actual_price = float(actual_price["price"])
            return actual_price
        info = client.get_symbol_info('BTCUSDT')
        min_indice = info['filters'][3]['minNotional']
        low_price = input("Lower price : ")
        highprice = input("Highest price: ")
        grid_qty = input("Grid quantity (5, 10...): ")
        quantity_per_grid = input(f"Quantity/Grid {min_indice}:")
        lev = input("Leverage value (1, 2, 10...) : ")
        alone_value = current_price(currency)
        alone_value = float("{0:.4f}".format(alone_value * sell_profit_percent))
        qty = float(price / alone_value)
        try :
            client.futures_change_leverage(symbol=currency, leverage=lev)
            # qty = 
            inter = quantity_per_grid/2
            count = 0
            try: 
                for i in grid_qty:
                    count += 1
                    if count == inter:
                        client.create_order(
                        symbol=self.currency,
                        side=SIDE_SELL,
                        type=ORDER_TYPE_LIMIT,
                        timeInForce=TIME_IN_FORCE_GTC,
                        quantity=quantity_per_grid,
                        price=alone_value)
                                
            except :
                pass
        except :
            pass
    

        
        # min_indice = 
        # 
        
        
class Trade:
    def __init__(self, currency, qty, price ):
        self.currency = currency
        self.price = price
    def buy(self, currency, qty, price):
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
        
    def sell(self):
        pass


class DataStore:
    def __init__(self, currency):
        self.currency = currency



       
    # def do_order():
    #     pass