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


def check_order_status(currency):
    actual_orders = client.get_open_orders()
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
      return print(f"Order {actual_orders} already placed.")
    else :
      return print(f"Order placed with {actual_orders} ORDER UID")
    time.sleep(0.1)

def get_crypto_conf():
  with open('config.json') as f:
    config = json.load(f)

###################################################################################################
def buy(currency, price, buy_marge_percent):
        info = client.get_symbol_info(currency)
        minimum = info['filters'][2]['minQty']
        print(info['filters'][2]['minQty'])

        alone_value = current_price(currency)
        # 
        alone_value = float("{0:.4f}".format(alone_value * buy_marge_percent))
        qty = float(price / alone_value)
        qty = float("{0:.3f}".format(qty))
        if float(qty) < float(minimum):
          print("QTY < Minimum required, ERROR")
        else:
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
          print(order)
          orderid = order["orderId"]
          clientorderid = order["clientOrderId"]
          print(f"Trade UID  :: {orderid}")                            
          # print(order[0])
          # check_order_status(currency)
          trade_cycle("buy", currency, price, orderid)
        
def sell(currency, price, sell_profit_percent):
        info = client.get_symbol_info(currency)
        minimum = info['filters'][2]['minQty']
        print(info['filters'][2]['minQty'])
        
        alone_value = current_price(currency)
        #
        alone_value = float("{0:.4f}".format(alone_value * sell_profit_percent))
        qty = float(price / alone_value)
        qty = float("{0:.3f}".format(qty))
        if float(qty) < float(minimum):
          print("QTY < Minimum required, ERROR")
        else:
          print(f"Unit value {alone_value} ")
          print(f"with price {price}")
          print(f"quantity = {qty}")                          
          order = client.create_order(
                                        symbol=currency,
                                        side=SIDE_SELL,
                                        type=ORDER_TYPE_LIMIT,
                                        timeInForce=TIME_IN_FORCE_GTC,
                                        quantity=qty,
                                        price=alone_value)
          print(order)
          orderid = order["orderId"]
          clientorderid = order["clientOrderId"]
          print(f"Trade UID  :: {orderid}")                            
          # print(order[0])
          # check_order_status(currency)
          trade_cycle("sell", currency, price, orderid)

def check_order_activity(currency, orderid):
    activity = client.get_order(
                            symbol=currency,
                            orderId=orderid)
    print(activity)
    # clientorderid
    if activity["status"] == "NEW":
      return "NEW"
    elif activity["status"] == "CANCELED":
      return "CANCELED"
    else : 
      print("Error in check_order_activity function")

def trade_cycle(last_order_type, currency, price, orderid):
  time.sleep(5)
  print("trade_cycle()")
  print(orderid)
  while True:
    status = check_order_activity(currency, orderid)
    print(status)

    if status == "NEW":
      time.sleep(2)
      print(f"order activity state : {status}")
    else :
      # last_order_type need to be BUY or SELL
      if last_order_type == "buy":
        buy(currency, price, buy_marge_percent)
        break
      if last_order_type == "sell":
        sell(currency, price,sell_profit_percent)
        break
      else : 
        print("ERROR ORDER TYPE IN trade_cycle() FUNCTION !")
        break

###################################################################################################
def main():
    trade1 = "sell" # Buy or Sell
    BANK = float(11)
    global sell_profit_percent, buy_marge_percent, last_type
    last_type = trade1
    sell_profit_percent = float(1.015)
    buy_marge_percent = float(0.995)
    currency = "BNBUSDT"

    if trade1 == "buy":
      buy(currency, BANK, buy_marge_percent)
    elif trade1 == "sell":
      sell(currency, BANK, sell_profit_percent)
    else:
      print("Error with trade1 var, must choice btw buy and sell")


    # actual_price = current_price(currency)
    # open_orders = client.get_open_orders()
    # print(open_orders)
    # if currency in open_orders:
    #   print(f"There is already an order for {currency} currency, IT'S NEED TO BE EMPTY !")

if __name__ == "__main__":
    main()