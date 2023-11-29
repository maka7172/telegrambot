import telebot
import requests
from .token1 import Token1


TOKEN = Token1.token()
NAVASAN_TOKEN = Token1.nava_token()
COIN_MARKET_CAP_KEY = Token1.coin_token()

bot = telebot.TeleBot(TOKEN)
ACTIVE_LIST = ['بازار داخلی','رمز ارز']

dakheli_list = ['usd','sekkeh','nim','dirham_dubai','منوی اصلی']
crypto_list = ['BTC','ETH','XRP','BNB','SOL','ADA','TRX','TON','LINK','BACK']


def start(message) :
    key_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=4)
    for i in ACTIVE_LIST :
        key_markup.add(i)
    bot.send_message(message.chat.id,'SELECT!!',reply_markup= key_markup)

def dakheli(message) :
    dakheli_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True,row_width=4)
    for i in dakheli_list :
            dakheli_markup.add(i)
    bot.send_message(message.chat.id,'بازار داخلی',reply_markup= dakheli_markup)

def crypto(message) :
    crypto_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True,row_width=4)
    for i in crypto_list :
        crypto_markup.add(i)
    bot.send_message(message.chat.id,'رمز ارز',reply_markup= crypto_markup) 

def get_crypto(message):
    symbol = message.text.upper()
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    parameters = {
        "symbol": symbol,  # نماد ارز رمزی
        "convert": "USD",  # واحد پول تبدیلی
                }
    headers = {
        "X-CMC_PRO_API_KEY": COIN_MARKET_CAP_KEY 
        }
    response = requests.get(url, params=parameters, headers=headers)
    result = response.json()
    result_price = result['data'][symbol]['quote']['USD']['price']
    return result_price
def get_dakheli(message):
    symbol = message.text.lower()  
    
    params={   
               'api_key' : NAVASAN_TOKEN ,
               'item' : message.text,              
             }
    r = requests.get('http://api.navasan.tech/latest/',params=params)
    result = r.json()
    result_price = result[symbol]['value']
    return result_price


@bot.message_handler(commands=['start'])
def send_welcome(message):
    name = bot.get_me()
    bot.send_message(message.chat.id,f"welcom to {name.first_name} bot!!!")
    start(message)

@bot.message_handler(func=lambda message: True)
def echo_all(message):    
    
    if message.text == 'بازار داخلی' :
        
       dakheli(message)
    
    elif message.text == 'رمز ارز' :
        
        crypto(message)

    elif message.text.upper() in crypto_list :
        if message.text == 'BACK' :
            start(message)
        else :
            result_price = get_crypto(message)       
            bot.send_message(message.chat.id,f"{result_price:.2f}")
    
    elif message.text.lower() in dakheli_list :
        if message.text == 'منوی اصلی' :
            start(message)
        else :
            result_price = get_dakheli(message)        
            bot.send_message(message.chat.id,result_price)
            
    else : 
        bot.send_message(message.chat.id,"please select from list")



bot.polling()