from collections import Counter
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Account, Transaction
from .utils import get_ticker_price

__all__ = ['buy', 
		   'sell',
		   'create_trader', 
		   'get_portfolio',
		   'get_log']

# Helpful link for inserting: https://stackoverflow.com/questions/7889183/sqlalchemy-insert-or-update-example
engine = create_engine(f'postgresql://Chuck:{os.environ["DB_PASS"]}@localhost/Chuck')
Session = sessionmaker(bind=engine)
session = Session()

def _get_aggregate_transactions(name, session=session):

	c = Counter()

	for row in session.query(Transaction).filter_by(name=name).all():

		c[row.ticker] += row.quantity

	return c

def get_portfolio(name, session=session):

	trader = session.query(Account).filter_by(name=name).first()

	if not trader:

		print(f'Account {name!r} does not exist')
		return

	delta_balance = 0

	for row in session.query(Transaction).filter_by(name=name).all():

		if row.action == 'BUY':

			delta_balance -= row.share_price * row.quantity

	total_value = 0

	for ticker, quantity in sorted(_get_aggregate_transactions(name).items()):

		print(ticker, '=', quantity)

		total_value += get_ticker_price(ticker=ticker) * quantity

	print('Net balance', '=', f'{trader.balance + delta_balance:,.2f}')
	print('Total value', '=', f'{trader.balance + delta_balance + total_value:,.2f}')

def get_log(name, sesson=session):

	for each in session.query(Transaction).filter_by(name=name).all():

		# transaction_date      |  name   | action | ticker | quantity | share_price
		print(each.transaction_date, each.action, each.ticker, each.quantity, each.share_price, sep=',')

def buy(name, ticker, quantity, session=session):

	trader = session.query(Account).filter_by(name=name).first()

	if not trader:

		print(f'Trader {name!r} does not exist')
		return

	share_price = get_ticker_price(ticker)

	if trader.balance < quantity * share_price:

		print('Cannot complete transaction, not enough money')

	else:
		
		t = Transaction.buy(name=name, ticker=ticker, quantity=quantity, share_price=share_price)

		trader.balance -= quantity * share_price

		session.add(trader)
		session.add(t)
		session.commit()

def sell(name, ticker, quantity, session=session, dry_run=True):

	trader = session.query(Account).filter_by(name=name).first()

	if not trader:

		print(f'Trader {name!r} does not exist')
		return
	
	share_price = get_ticker_price(ticker)

	c = _get_aggregate_transactions(name=name)

	# Sell all stock shares if the shares requested is greater than what is in the portfolio
	quantity = quantity if c[ticker] > quantity else c[ticker]

	if dry_run: 
		
		print('SELLING', ticker, quantity)
		exit()

	t = Transaction.sell(name=name, ticker=ticker, quantity=quantity, share_price=share_price)

	trader.balance += quantity * share_price

	session.add(trader)
	session.add(t)
	session.commit()

def create_trader(name, balance, session=session):

	t = Account(name=name, balance=balance)

	session.add(t)

	session.commit()