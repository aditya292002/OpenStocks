from sqlalchemy import func
from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Stock(Base):
    __tablename__ = 'stocks'

    StockID = Column(Integer, primary_key=True, autoincrement=True)
    StockSymbol = Column(String(10), nullable=False)
    CompanyName = Column(String(255), nullable=False)
    # CurrentPrice = Column(DECIMAL(10, 2), nullable=False)

class User(Base):
    __tablename__ = 'users'

    UserID = Column(Integer, primary_key=True, autoincrement=True)
    UserName = Column(String(255), nullable=False)
    CurrentBalance = Column(DECIMAL(15, 2), nullable=False)

class UserStocks(Base):
    __tablename__ = 'user_stocks'

    OwnershipID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('users.UserID'), nullable=False)
    StockID = Column(Integer, ForeignKey('stocks.StockID'), nullable=False)
    QuantityOwned = Column(Integer, nullable=False)

    user = relationship('User', back_populates='stocks')
    stock = relationship('Stock', back_populates='owners')


class Order(Base):
    __tablename__ = 'orders'

    OrderID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('users.UserID'), nullable=False)
    StockID = Column(Integer, ForeignKey('stocks.StockID'), nullable=False)
    OrderType = Column(String(10), nullable=False)
    Quantity = Column(Integer, nullable=False)
    Price = Column(DECIMAL(10, 2), nullable=False)
    OrderStatus = Column(String(20), nullable=False)
    Timestamp = Column(TIMESTAMP, default=func.now(), nullable=False)
    user = relationship('User', back_populates='orders')
    stock = relationship('Stock', back_populates='orders')
