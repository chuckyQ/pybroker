from sqlalchemy import create_engine, Column, Integer, String, Sequence, Float
from sqlalchemy.ext.declarative import  declarative_base
from datetime import datetime
import os

Base = declarative_base()

POSSIBLE_ACTIONS = ['BUY', 'SELL']

class Account(Base):

    __tablename__ = 'traders'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(25), unique=True)
    balance = Column(Float())

    def __init__(self, name, balance):

        self.name = name
        self.balance = balance

    def __repr__(self):

        return f'{self.__class__.__name__}(id={self.id}, name={self.name}, balance="${self.balance:,.2f}")'

class Transaction(Base):

    __tablename__ = 'transaction'

    id = Column(Integer, Sequence('transaction_id_seq'), primary_key=True)
    transaction_date = Column(String(26)) # '2019-06-27T23:35:18.247265'
    name = Column(String(25)) # name from the Trader database
    action = Column(String(4)) # BUY or SELL
    ticker = Column(String(10)) # Overkill for a ticker but it works
    quantity = Column(Integer())
    share_price = Column(Float())

    def __init__(self, name, action, ticker, quantity, share_price):

        if action not in POSSIBLE_ACTIONS:

            raise ValueError(f'{action!r} is not in {POSSIBLE_ACTIONS}')

        self.name = name
        self.action = action
        self.ticker = ticker.upper() # I am pretty sure stock tickers are case insensitive so normalization should be ok
        self.quantity = quantity
        self.share_price = share_price
        self.transaction_date = datetime.now().isoformat()

    @classmethod
    def buy(cls, name, ticker, quantity, share_price):

        return Transaction(name=name, 
                           action='BUY', 
                           ticker=ticker, 
                           quantity=quantity, 
                           share_price=share_price)

    @classmethod
    def sell(cls, name, ticker, quantity, share_price):

        return Transaction(name, 
                           action='SELL', 
                           ticker=ticker, 
                           quantity=quantity, 
                           share_price=share_price)
 
if __name__ == "__main__":

    engine = create_engine(f'postgresql://Chuck:{os.environ["DB_PASS"]}@localhost/Chuck', echo=True)

    Base.metadata.create_all(engine)