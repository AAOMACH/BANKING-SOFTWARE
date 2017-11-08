import os
import sys
from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Bank(Base):
    __tablename__ = 'bank'
    bank_id = Column(Integer, primary_key=True)
    bank_name = Column(String(250), nullable=False)
    bank_location = Column(String(259), nullable=False)
    # creating the one to many relationship btn bank and teller
    tellers1 = relationship("Teller", back_populates="bank")
    # creating the one to many relationship btn bank and customer
    customers1 = relationship("Customer", back_populates="bank")



# creating the association table
association_table = Table('association', Base.metadata,
                          Column('left_id', Integer, ForeignKey('left.id')),
                          Column('right_id', Integer, ForeignKey('right.account_number'))
                          )


class Teller(Base):
    __tablename__='left'
    id = Column(Integer,primary_key=True)
    teller_name = Column(String(250), nullable=False)
    # creating the one to many relationship btn bank and teller
    teller_id = Column(Integer, ForeignKey('bank.bank_id'))
    bank = relationship("Bank", back_populates="tellers1")
    # creating the many to many relationship
    customers = relationship("Customer",
                             secondary=association_table,
                             back_populates="tellers")


class Customer(Base):
    __tablename__='right'
    account_number = Column(Integer, primary_key=True)
    account_name = Column(String(250), nullable=False)
    phone_number = Column(Integer, nullable=True)
    account_type = Column(String(250), nullable=False)
    balance = Column(Integer, nullable=False)
    loan = Column(Integer, nullable=True)
    # creating the many to many relationship
    tellers = relationship("Teller",
                           secondary=association_table,
                           back_populates="customers")
    # creating the one to many relationship btn customer and account
    accounts = relationship("Account", back_populates="customer")
    # creating the one to many relationship btn bank and customer
    customer_id = Column(Integer, ForeignKey('bank.bank_id'))
    bank = relationship("Bank", back_populates="customers1")



class Account(Base):
    __tablename__ = 'acc_type'
    id = Column(Integer, primary_key=True)
    acc_type = Column(String, nullable=False)
    # creating the one to many relationship btn customer and account
    customer_id = Column(Integer, ForeignKey('right.account_number'))
    customer = relationship("Customer", back_populates="accounts")

class Card_Application(Base):
    __tablename__='card_application'
    card_number = Column(Integer, primary_key=True)
    account_number = Column(Integer, nullable=False)
    account_name = Column(String(250), nullable=False)
    reason_for = Column(String(250), nullable=False)
    issued_card = Column(String(250),nullable = True)

class Loan(Base):
    __tablename__="Loan"
    loan_id = Column(Integer, primary_key=True)
    account_name=Column(String(250), nullable=False)
    account_number = Column(Integer, nullable=True)
    Security = Column(String(250), nullable=False)
    amount = Column(Integer, nullable=False)
    date_pay = Column(String, nullable=False)

class Transactions(Base):
    __tablename__= 'transact'
    id = Column(Integer, primary_key=True)
    type_trans = Column(String(250), nullable=False)
    account_number = Column(Integer, nullable=False)
    teller_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)

# Create an engine that stores data in the local directory's bank.db file.


engine = create_engine('sqlite:///bank.db')

# Create all tables in the engine. This is equivalent to "Create Table"
Base.metadata.create_all(engine)