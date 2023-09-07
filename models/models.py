from configuration.imports import *
Base = declarative_base()

class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer(), primary_key=True)
    customer_id = Column(Integer(), ForeignKey('customers.id'), nullable=False)
    product_id = Column(Integer(), ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer())
    purchase_date = Column(DateTime(), server_default=func.now())

    # create class relationships as attributes
    customer = relationship('Customer', back_populates='purchases')
    product = relationship('Product', back_populates='purchases')

    def __repr__(self):
        return f'({self.id}) {self.customer_id} {self.product_id} {self.quantity} {self.purchase_date}'


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    full_name = Column(String(), default=lambda c: f'{c.first_name} {c.last_name}')
    loyalty_points = Column(Integer())

    purchases = relationship('Purchase', back_populates='customer', cascade='all, delete-orphan')
    products = association_proxy("purchases", "product")

    @property
    def full_names(self):
        return f'{self.first_name} {self.last_name}'


    def __repr__(self):
        return f'({self.id}) {self.full_name} - Loyalty Points: {self.loyalty_points}'


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

    purchases = relationship('Purchase', back_populates='product')
    customers = association_proxy('purchases', 'customer')


    def __repr__(self):
        return f'({self.id}): Name:{self.name} | Price:{self.price} | Quantity:{self.quantity} | Category:{self.category.name} | Supplier:{self.supplier.name}'


class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    products = relationship('Product', back_populates='supplier', cascade='all, delete-orphan')

    def __repr__(self):
        return f'({self.id}) {self.name}\n'


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    products = relationship('Product', back_populates='category', cascade='all, delete-orphan')

    def __repr__(self):
        return f'({self.id}) {self.name}\n'

class User(Base):

    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    customer_id = Column(Integer(), ForeignKey('customers.id'))
    username = Column(String())
    password = Column(String())
    role = Column(String())

    def __repr__(self):
        return f'({self.id}) {self.username} Role:{self.role}\n'


