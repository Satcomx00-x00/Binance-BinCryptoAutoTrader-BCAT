from pytglib.client import Telegram

# Change the values below
api_id = 2897881
api_hash = 'ab1cc2521c4daaa132531528e9082788'
phone_number = '+12312312312'
dbenc = '32_hexademical_chars'

# Initiate the client
client = Telegram(api_id=api_id, api_hash=api_hash, phone=phone_number, database_encryption_key=dbenc)

# Login to the client
client.login()

# Define the handler function
def my_message_handler(update):
    print(update)

# Register it
client.add_message_handler(my_message_handler)

tg.idle()

# And you're ready to go!