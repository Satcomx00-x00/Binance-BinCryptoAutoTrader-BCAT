import json
import os
import time
from time import sleep
from datetime import datetime


from binance.websockets import BinanceSocketManager
from binance.client import Client
from binance.enums import *

from colorama import Back, Fore, Style, init
from prettytable import PrettyTable
x = PrettyTable()
os.system('cls')

init()
actual_time = datetime.now()
print(f"Program start timestamp : {actual_time}")

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
def buy(currency, price, buy_marge_percent,state):
        if state == True:
          alone_value = current_price(currency)
          alone_value = alone_value * BANK
        else :
          alone_value = current_price(currency)
        info = client.get_symbol_info(currency)
        minimum = info['filters'][2]['minQty']
        print("-----------------------------------")
        print(info['filters'][2]['minQty'])

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
          orderid = order["orderId"]
          clientorderid = order["clientOrderId"]
          print(f"Trade UID  :: {orderid}")                            
          print("-----------------------------------")
          trade_cycle("buy", currency, price, orderid)
        
def sell(currency, price, sell_profit_percent, state):
        if state == True:
          alone_value = current_price(currency)
          alone_value = alone_value * BANK
        else :
          alone_value = current_price(currency)
        info = client.get_symbol_info(currency)
        minimum = info['filters'][2]['minQty']
        print("-----------------------------------")
        print(info['filters'][2]['minQty'])
        
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
          orderid = order["orderId"]
          clientorderid = order["clientOrderId"]
          print(f"Trade UID  :: {orderid}")                            
          print("-----------------------------------")
          trade_cycle("sell", currency, price, orderid)


def check_order_activity(currency, orderid):
  try:
      activity = client.get_order(
                              symbol=currency,
                              orderId=orderid)

      if activity["status"] == "NEW":
        return "NEW"
      else :
        return "CANCELED"
  except :
      time.sleep(1)
      check_order_activity(currency, orderid)

def trade_cycle(last_order_type, currency, price, orderid):
  time.sleep(5)
  while True:
    status = check_order_activity(currency, orderid)

    if status == "NEW":
      time.sleep(2)
      if last_order_type == "sell":
          print(f"order activity state {Fore.YELLOW}{status}{Style.RESET_ALL} With Type {Fore.RED}{last_order_type}{Style.RESET_ALL}")
      elif last_order_type == "buy":
          print(f"order activity state {Fore.YELLOW}{status}{Style.RESET_ALL} With Type {Fore.GREEN}{last_order_type}{Style.RESET_ALL}")

    elif status == "CANCELED":
      print(f"order activity state {Fore.YELLOW}{status}{Style.RESET_ALL} With Type {Fore.RED}{last_order_type}{Style.RESET_ALL}")
      if last_order_type == "buy":
        print(datetime.now())
        sell(currency, price, buy_marge_percent, state)
        break
      elif last_order_type == "sell":
        print(datetime.now())
        buy(currency, price,sell_profit_percent, state)
        break
      else : 
        print("ERROR ORDER TYPE IN trade_cycle() FUNCTION !")
        break

def wallet_loader():
    BTC_balance = client.get_asset_balance(asset='BTC')
    USDT_balance = client.get_asset_balance(asset='USDT')
    BNB_balance = client.get_asset_balance(asset='BNB')
    ETH_balance = client.get_asset_balance(asset='ETH')

    x.field_names = ["Curency", "Free", "Locked"]
    x.add_rows(
        [
            ["BTC", Fore.GREEN+BTC_balance['free']+Style.RESET_ALL, Fore.YELLOW+BTC_balance['locked']+Style.RESET_ALL],
            ["USDT", Fore.GREEN+USDT_balance['free']+Style.RESET_ALL, Fore.YELLOW+USDT_balance['locked']+Style.RESET_ALL],
            ["BNB", Fore.GREEN+BNB_balance['free']+Style.RESET_ALL, Fore.YELLOW+BNB_balance['locked']+Style.RESET_ALL],
            ["ETH", Fore.GREEN+ETH_balance['free']+Style.RESET_ALL, Fore.YELLOW+ETH_balance['locked']+Style.RESET_ALL],
        ]
    )
    print(x)

###################################################################################################
def main():
    global sell_profit_percent, buy_marge_percent, last_type, BANK, state
    wallet_loader()
    trade1 = "sell" # Buy or Sell
    currency = "BNBUSDT"

    BANK = float(10)
    sell_profit_percent = float(1.001)
    buy_marge_percent = float(0.999)
    # # # # # # # # # # # # # # # #  DON'T TOUCH UNDER THIS LINE # # # # # # # # # # # # # # # # 
    state = False
    last_type = trade1
    if trade1 == "buy":
      buy(currency, BANK, buy_marge_percent, state)
    elif trade1 == "sell":
      sell(currency, BANK, sell_profit_percent,state)
    else:
      print("Error with trade1 var, must choice btw buy and sell")

if __name__ == "__main__":
    main()



    # info = client.get_account()
    # print(" ╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮")
    # print(f"     ACCOUNT ASSETs BALANCES        ")
    # print(f"  BTC  ↘                             ")
    # print(f"        Free: {btc_balance['free']} ")
    # print(f"        Locked:{btc_balance['locked']}")
    # print(f"  USDT ↘                             ")
    # print(f"        Free: {usdt_balance['free']} ")
    # print(f"        Locked:{usdt_balance['locked']}")
    # print(" ╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯")