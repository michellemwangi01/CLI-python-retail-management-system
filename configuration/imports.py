from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, func, Table, DateTime, and_
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import sessionmaker, relationship, declarative_base


import click

import random

engine = create_engine('sqlite:///database/retail_store_management.db')
Session = sessionmaker(bind=engine)
session = Session()

