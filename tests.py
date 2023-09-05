from models import *
category_search_name = 'fresh'
supplier_products = session.query(Product).join(Product.category).filter(Category.name == 'Fresh Produce').all()
category_products = session.query(Product).join(Category.products).filter(Category.name.like(f'%{category_search_name}%')).all()

print(supplier_products)
print(category_products)