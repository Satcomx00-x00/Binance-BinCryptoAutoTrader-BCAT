from binance.client import Client
import json
from BCATlib import Misc

# from colorama import init, Fore, Back, Style
# init()

with open('config.json') as f:
  data = json.load(f)


client = Client(data["api_key"], data["api_secret"])


info = client.get_symbol_info('BNBBTC')
print(info)