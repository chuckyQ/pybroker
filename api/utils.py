"""Small utility module for grabbing the ticker price from 
Yahoo Finance.
"""

import json 
import requests

__all__ = ['get_ticker_price']

TICKER_URL_FMT = 'https://finance.yahoo.com/quote/{ticker}?p={ticker}'

TICKER_PRICE_CACHE = dict()

def get_ticker_price(ticker):
	"""Function for pulling the stock price from Yahoo Finance. Uses a cache
	to hold the stock price so as not to spam Yahoo Finance.
	:returns: the ticker price of the stock
	
	>>> get_ticker_price(ticker='F') #doctest: +SKIP
	10.23
	"""

	price = TICKER_PRICE_CACHE.get(ticker)

	if price is not None:

		return price

	url = TICKER_URL_FMT.format(ticker=ticker)

	req = requests.get(url)

	if req.status_code != 200:

		raise IOError(f'Could not find ticker {ticker!r}, verify the ticker is valid.')

	price = _get_ticker_price(req.text)

	TICKER_PRICE_CACHE[ticker] = price

	return price

def get_value(jsondata, *keys):
	"""Helpful function for recursively finding nested json data"""

	if len(keys) < 2:

		return jsondata[keys[0]]

	else:

		return get_value(jsondata[keys[0]], *keys[1:])

def _get_json_data(html):
	"""At the bottom of each stock html page, there is 
	a blob of json data and this function pulls that json 
	data out, given an html text.
	"""

	html = html.split('root.App.main = ')[1] # Pull the data side
	html = html.strip(';')
	html = html.split('}(this));')[0] # Isolate the json data

	html = html.strip().rstrip(';').strip() # Strip extraneous punctuation and whitespace

	return json.loads(html)

def _get_ticker_price(html):
	"""Internal function for parsing the html from the Yahoo Finance request.
	:returns: The stock price.
	"""

	jsondata = _get_json_data(html)

	return get_value(jsondata, 'context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'financialData', 'currentPrice', 'raw')