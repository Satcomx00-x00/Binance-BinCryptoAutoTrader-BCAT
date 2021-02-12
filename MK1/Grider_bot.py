
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


def current_price(currency):
    actual_price = client.get_symbol_ticker(symbol=currency)
    print(f'{currency} is actually {Fore.YELLOW}{actual_price["price"]}{Style.RESET_ALL}')
    # actual_price = actual_price["price"].replace(".",",")
    actual_price = float(actual_price["price"])
    return actual_price


def grid_gamble(currency, low_price, highprice, grid_qty, quantity_per_grid, lev):
    
    alone_value = current_price(currency)
    alone_value = float("{0:.4f}".format(alone_value * 0.01))
    print(alone_value)
    # try :
    # client.futures_change_leverage(symbol=currency, leverage=lev)
    # qty = 
    inter = quantity_per_grid/2
    count = 0
    # try: 
    while count < inter:
        count += 1
        print(count)

        if count <= inter:
            client.create_order(
            symbol=currency,
            side=SIDE_BUY,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=quantity_per_grid,
            price=alone_value)
        else:
            client.create_order(
            symbol=currency,
            side=SIDE_SELL,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=quantity_per_grid,
            price=alone_value)

                            
    #     except :
    #         pass
    # except :
    #     pass

def main():
    currency = input("Currency(BTCUSDT): ")
    
    info = client.get_symbol_info('BTCUSDT')
    min_indice = info['filters'][3]['minNotional']
    low_price = input("Lower price : ")
    highprice = input("Highest price: ")
    grid_qty = int(input("Grid quantity (5, 10...): "))
    quantity_per_grid = float(input(f"Quantity/Grid ({min_indice}):"))
    lev = input("Leverage value (1, 2, 10...) : ")
    grid_gamble(
        currency = currency,
        low_price = low_price,
        highprice = highprice,
        grid_qty = grid_qty,
        quantity_per_grid = quantity_per_grid,
        lev =lev
        )

if __name__ == "__main__":
    main()