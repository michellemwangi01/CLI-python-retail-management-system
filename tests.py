from models import *

supplier_products = session.query(Product).filter(Supplier.id == 24).all()

supplier = session.query(Supplier).filter(Supplier.id == 1).first()
print(supplier_products)
print(supplier)