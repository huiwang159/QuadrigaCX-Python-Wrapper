import requests
import time
import hmac
import hashlib

'''
----------
QuadrigaCX
----------
'''

client_id = ''
api_key = ''
api_secret = ''

bc = 'btc_cad'
bu = 'btc_usd'
eb = 'eth_btc'
ec = 'eth_cad'

'''
Parameters
----------
order_book: bc, bu, eb, ec

Returns
----------
JSON dictionary:
last - last BTC price
high - last 24 hours price high
low - last 24 hours price low
vwap - last 24 hours volume weighted average price: vwap
volume - last 24 hours volume
bid - highest buy order
ask - lowest sell order
'''
def current_trading_information(order_book):
    trading_information = requests.get('https://api.quadrigacx.com/v2/ticker?book=' + order_book).json()
    return trading_information

'''
Parameters
----------
order_book: bc, bu, eb, ec

Returns
----------
Returns JSON dictionary with "bids" and "asks". Each is a list of open orders and each order is represented as a list of price and amount.
'''
def order_book(order_book):
    payload = {'book': order_book}
    return requests.get('https://api.quadrigacx.com/v2/order_book', params=payload).json()

'''
Parameters
----------
book: bc, bu, eb, ec
time: minute, hour

Returns
----------
JSON dictionary:
date - unix timestamp date and time
tid - transaction id
price - BTC price
amount - BTC amount
side - The trade side indicates the maker order side (maker order is the order that was open on the order book)
'''
def transactions(order_book, time):
    my_payload = {'book': order_book, 'time': time}
    return requests.get('https://api.quadrigacx.com/v2/transactions', params=my_payload).json()

def payload():
    nonce = str(int(time.time()*1000))
    message = bytes(nonce + client_id + api_key, 'utf-8')
    secret = bytes(api_secret, 'utf-8')
    signature = hmac.new(secret, message, hashlib.sha256).hexdigest()
    payload = {}
    payload['key'] = api_key
    payload['nonce'] = nonce
    payload['signature'] = signature
    return payload

'''
Parameters
----------
key - API key
signature - signature
nonce - nonce

Returns
----------
JSON dictionary:
cad_balance - CAD balance
btc_balance - BTC balance
cad_reserved - CAD reserved in open orders
btc_reserved - BTC reserved in open orders
cad_available - CAD available for trading
btc_available - BTC available for trading
fee - customer trading fee
'''
def account_balance():
    return requests.post('https://api.quadrigacx.com/v2/balance', json=payload()).json()

'''
Parameters
----------
key - API key
signature - signature
nonce - nonce
offset - skip that many transactions before beginning to return results. Default: 0.
limit - limit result to that many transactions. Default: 100.
sort - sorting by date and time (asc - ascending; desc - descending). Default: desc.
book - optional, if not specified, will default to btc_cad

Returns
----------
JSON dictionary:
datetime - date and time
id - unique identifier (only for trades)
type - transaction type (0 - deposit; 1 - withdrawal; 2 - trade)
method - deposit or withdrawal method
(minor currency code) – the minor currency amount
(major currency code) – the major currency amount
order_id - a 64 character long hexadecimal string representing the order that was fully or partially filled (only for trades)
fee – transaction fee
rate – rate per btc (only for trades)
'''
def user_transactions(offset, limit, sort, book):
    my_payload = payload()
    my_payload['offset'] = offset
    my_payload['limit'] = limit
    my_payload['sort'] = sort
    my_payload['book'] = book
    return requests.post('https://api.quadrigacx.com/v2/user_transactions', json=my_payload).json()

'''
Parameters
----------
order_book: bc, bu, eb, ec

Returns
----------
JSON dictionary:
id - order id
datetime - date and time
type - buy or sell (0 - buy; 1 - sell)
price - price
amount - amount
status - status of the order (0 - active; 1 - partially filled)
'''
def open_orders(book):
    my_payload = payload()
    my_payload['book'] = book
    return requests.post(url='https://api.quadrigacx.com/v2/open_orders', json=my_payload).json()

'''
Parameters
----------
key - API key
signature - signature
nonce - nonce
id – a single or array of 64 characters long hexadecimal string taken from the list of orders

Returns
----------
JSON dictionary:
id - the order id passed to that function
book - which orderbook it belongs to
price - price of the order
amount - amount of the order
type - buy or sell (0 - buy; 1 - sell)
status - status of the order (-1 - canceled; 0 - active; 1 - partially filled; 2 - complete)
created - date the order was created
updated - date the order was last updated (not shown when status = 0)
'''
def lookup_order(id):
    my_payload = payload()
    my_payload['id'] = id
    return requests.post('https://api.quadrigacx.com/v2/lookup_order', json=my_payload).json()

'''
Parameters
----------
JSON dictionary:
key - API key
signature - signature
nonce - nonce
id – a 64 characters long hexadecimal string taken from the list of orders

Returns
----------
Returns 'true' if order has been found and canceled.
'''
def cancel_order(id):
    my_payload = payload()
    my_payload['id'] = id
    return requests.post('https://api.quadrigacx.com/v2/cancel_order', json=my_payload).json()

'''
Parameters
----------
key - API key
signature - signature
nonce - nonce
amount - amount of major currency
price - price to buy at
book - optional, if not specified, will default to btc_cad

Returns
----------
JSON dictionary:
id - order id
datetime - date and time
type - buy or sell (0 - buy; 1 - sell)
price - price
amount - amount
'''
def buy_order(order_book, price, amount):
    my_payload = payload()
    my_payload['book'] = order_book
    my_payload['price'] = price
    my_payload['amount'] = amount
    return requests.post(url='https://api.quadrigacx.com/v2/buy', json=my_payload).json()

'''
Parameters
----------
key - API key
signature - signature
nonce - nonce
amount - amount of major currency
price - price to sell at
book - optional, if not specified, will default to btc_cad

Returns
----------
JSON dictionary:
id - order id
datetime - date and time
type - buy or sell (0 - buy; 1 - sell)
price - price
amount - amount
'''
def sell_order(book, amount, price):
    my_payload = payload()
    my_payload['amount'] = amount
    my_payload['price'] = price
    my_payload['book'] = book
    return requests.post('https://api.quadrigacx.com/v2/sell', json = my_payload).json()

'''
Parameters
----------
key - API key
signature - signature
nonce - nonce

Returns
----------
Returns a bitcoin deposit address for funding your account.
'''
def bitcoin_deposit():
    my_payload = payload()
    return requests.post('https://api.quadrigacx.com/v2/bitcoin_deposit_address', json=my_payload).json()

'''
Parameters
----------
key - API key
signature - signature
nonce - nonce
amount – The amount to withdraw
address – The bitcoin address we will send the amount to

Returns
----------
OK or error
'''
def bitcoin_withdraw(amount, address):
    my_payload = payload()
    my_payload['amount'] = amount
    my_payload['address'] = address
    return requests.post('https://api.quadrigacx.com/v2/bitcoin_withdrawal', json=my_payload).json()

'''
Parameters
----------
key - API key
signature - signature
nonce - nonce

Returns
----------
Returns the ethereum deposit address for funding your account.
'''
def ether_deposit():
    my_payload = payload()
    return requests.post('https://api.quadrigacx.com/v2/ether_deposit_address', json = my_payload).json()

'''
Parameters
----------
key - API key
signature - signature
nonce - nonce
amount – The amount to withdraw
address – The ethereum address we will send the amount to

Returns
----------
OK or error
'''
def ether_withdraw(amount, address):
    my_payload = payload()
    my_payload['amount'] = amount
    my_payload['address'] = address