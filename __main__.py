"""
Command line interface for buying and selling stocks

Usage:
  main.py (buy | sell) <name> <ticker> -q QUANTITY
  main.py (portfolio | log) <name>
  main.py create_trader <name> -b BALANCE

Options:
  -q QUANTITY, --quantity=<quantity>  Purchase a quantity of shares of ticker
  -b BALANCE                         Starting balance for user
"""

from docopt import docopt

from .api import (buy, 
				  sell,
				  create_trader,
				  get_portfolio,
				  get_log
				  )

from .api.utils import get_ticker_price

options = docopt(__doc__)

if options['portfolio']:

	get_portfolio(name=options['<name>'])

elif options['log']:

	get_log(name=options['<name>'])

elif options['buy']:

	buy(name=options['<name>'],
		ticker=options['<ticker>'],
		quantity=int(options['--quantity']))

elif options['sell']:

	sell(name=options['<name>'],
		 ticker=options['<ticker>'],
		 quantity=int(options['--quantity']))

elif options['create_trader']:

	create_trader(name=options['<name>'])
