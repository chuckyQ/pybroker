"""
Command line interface for buying and selling stocks

Usage:
  main.py (buy | sell) <name> <ticker> -q QUANTITY
  main.py (portfolio | log | balance) <name>
  main.py create_trader <name> -b BALANCE

Options:
  -q QUANTITY, --quantity=<quantity>  Purchase a quantity of shares of ticker
  -b BALANCE                         Starting balance for user
"""

from docopt import docopt

from .api import (buy, 
				  create_trader,
				  get_portfolio,
				  get_log
				  )

from .api.utils import get_ticker_price

options = docopt(__doc__)

TRANSACTION_TEMPLATE = '{ticker:<10}{sep}{quantity:<20}{sep}{total_value:<20}{sep}'
SEPARATOR = TRANSACTION_TEMPLATE.format(ticker='-' * 10, quantity='-' * 20, total_value='-' * 20, sep='+')

if options['portfolio']:

	get_portfolio(name=options['<name>'])

elif options['log']:

	get_log(name=options['<name>'])

elif options['balance']:

	get_balance_sheet(name=options['<name>'])

elif options['buy']:

	buy(name=options['<name>'],
		ticker=options['<ticker>'],
		quantity=int(options['QUANTITY']))

elif options['sell']:

	pass

elif options['create_trader']:

	create_trader(name=options['<name>'])
