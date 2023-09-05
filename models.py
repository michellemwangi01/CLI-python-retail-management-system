from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base


engine = create_engine('sqlite:///retail_store_management.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    products = relationship('Product', back_populates='category')

    def __repr__(self):
        return f'({self.id}) {self.name}\n'


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    category_id = Column(Integer(), ForeignKey("categories.id"))
    price = Column(Integer())
    quantity = Column(Integer())
    supplier_id = Column(Integer(), ForeignKey("suppliers.id"))

    category = relationship('Category', back_populates='products')
    supplier = relationship('Supplier', back_populates='products')

    def __repr__(self):
        return f'({self.id}) {self.name}, {self.price}, {self.quantity}\n'


class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    products = relationship('Product', back_populates='supplier')

    def __repr__(self):
        return f'({self.id}) {self.name}'
