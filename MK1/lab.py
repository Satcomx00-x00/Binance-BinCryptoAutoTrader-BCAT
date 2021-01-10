import json
import os
import time
from time import sleep

from binance.client import Client
from binance.enums import *
from colorama import Back, Fore, Style, init

init()
# from colorama import init, Fore, Back, Style
# init()
os.system('cls')
with open('config.json') as f:
  data = json.load(f)
client = Client(data["api_key"], data["api_secret"])
###################################################################################################
def current_price(currency):
    actual_price = client.get_avg_price(symbol=currency)
    print(f'{currency} is actually {Fore.YELLOW}{actual_price["price"]}{Style.RESET_ALL}')
    # actual_price = actual_price["price"].replace(".",",")
    actual_price = float(actual_price["price"])
    return actual_price

def check_order_activity(currency, orderid):
  order = client.get_order(
                            symbol=currency,
                            orderId=orderid)

def check_order_status(currency):
    actual_orders = client.get_open_orders()
    # print(actual_orders)
    # out=' '.join(map(str, actual_orders))
    # print(out)
    
    # actual_orders=json.dumps(out)
    # print(actual_orders['orderId'])

    print (actual_orders)

    actual_orders = str(actual_orders)
    symbol = str(actual_orders)

    pos1 = symbol.find("symbol': ")
    pos2 = symbol.find("', 'orderId'")
    symbol = symbol[pos1:pos2]
    symbol = symbol.replace("symbol': '","")
    print(symbol)

    pos1 = actual_orders.find("orderId': ")
    pos2 = actual_orders.find(", 'orderListId")
    actual_orders = actual_orders[pos1:pos2]
    actual_orders = actual_orders.replace("orderId': ","")
    print (actual_orders)

    # print(actual_orders)
    print(f"{symbol} {currency}")
    if symbol != currency:
        print(f"Order {actual_orders} already placed.")
    else :
      return print(f"Order placed with {actual_orders} ORDER UID")
    time.sleep(0.1)
    check_order_status(currency)

###################################################################################################
def buy(currency, price):
        alone_value = current_price(currency)
        # 
        alone_value = float("{0:.2f}".format(alone_value * 0.98))
        qty = float(price / alone_value)
        qty = float("{0:.5f}".format(qty))
        print(f"alone_value {alone_value} ")
        print(f"with price {price}")
        print(f"qty = {qty}")                          
        order = client.create_order(
                                      symbol=currency,
                                      side=SIDE_BUY,
                                      type=ORDER_TYPE_LIMIT,
                                      timeInForce=TIME_IN_FORCE_GTC,
                                      quantity=qty,
                                      price=alone_value)
        check_order_status(currency)
        trade_cycle("buy", currency, price)
        
def sell(currency, price):
        alone_value = current_price(currency)
        # 
        alone_value = float("{0:.2f}".format(alone_value * 1.01))
        qty = float(price / alone_value)
        qty = float("{0:.5f}".format(qty))
        print(f"alone_value {alone_value} ")
        print(f"with price {price}")
        print(f"qty = {qty}")                          
        order = client.create_order(
                                      symbol=currency,
                                      side=SIDE_SELL,
                                      type=ORDER_TYPE_LIMIT,
                                      timeInForce=TIME_IN_FORCE_GTC,
                                      quantity=qty,
                                      price=alone_value)
        check_order_status(currency)
        trade_cycle("sell", currency, price)
            
def trade_cycle(last_order_type, currency, price):
  # last_order_type need to be BUY or SELL
  if last_order_type == "buy":
    buy(currency, price)
  if last_order_type == "sell":
    sell(currency, price)
  else : 
    print("ERROR ORDER TYPE IN trade_cycle() FUNCTION !")
    

###################################################################################################
def main():
    # actual_price = client.get_avg_price(symbol='BNBBTC')
    trade1 = "buy" # Buy or Sell
    BANK = float(10)
    currency = "MKRUSDT"

    
    # sellpercent = float()
    # buypercent = float()

    if trade1 == "buy":
      buy(currency,BANK)
    elif trade1 == "sell":
      sell(currency,BANK)
    else:
      print("Error with trade1 var, must choice btw buy and sell")
      

    # actual_price = current_price(currency)
    # open_orders = client.get_open_orders()
    # print(open_orders)
    # if currency in open_orders:
    #   print(f"There is already an order for {currency} currency, IT'S NEED TO BE EMPTY !")

 

if __name__ == "__main__":
    main()