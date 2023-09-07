import datetime

from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, func, Table, DateTime, and_
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

import random

import click

engine = create_engine('sqlite:///retail_store_management.db')
Session = sessionmaker(bind=engine)
session = Session()

