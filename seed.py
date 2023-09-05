from faker import Faker
import random

from models import *

fake = Faker()

categories = ["Fresh Produce", "Dairy Products", "Bakery Items", "Meat and Poultry", "Seafood", "Canned Goods",
              "Frozen Foods", "Snack Foods", "Beverages", "Condiments and Sauces", "Cereal and Breakfast Foods",
              "Pasta and Rice", "Canned and Dried Beans", "Personal Care Products", "Cleaning Supplies", "Paper Products",
              "Health and Wellness", "Pet Supplies", "Household Goods", "Baby Care Products"]
suppliers = ["GreenGrocer Suppliers", "FreshHarvest Foods", "QualityProvisions Co.","PantryMaster Distributors","FarmToTable Supplies","Gourmet Essentials Ltd.","PrimeGrocery Suppliers","MegaMart Wholesalers","EpicProduce Distributors","PremiumPantry Imports"]

if __name__ == '__main__':
    engine = create_engine('sqlite:///retail_store_management.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Product).delete()
    session.query(Supplier).delete()
    session.query(Category).delete()

    '''----------------------- C A T E G O R I E S ______________________--'''
    for item in categories:
        new_category = Category(
            name=item
        )
        session.add(new_category)
        session.commit()
    print("Category import complete.")

    '''----------------------- S U P P L I E R S ______________________--'''
    for item in suppliers:
        new_supplier = Supplier(
            name=item
        )
        session.add(new_supplier)
        session.commit()
    print("Supplier import complete.")

    '''----------------------- P R O D U C T S ______________________--'''
    products = []
    for item in categories:
        for i in range(random.randint(1,10)):
            supplier = session.query(Supplier).order_by(func.random()).first()
            category = session.query(Category).order_by(func.random()).first()
            new_product = Product(
                name = fake.name(),
                price=round(random.uniform(100,1000),2),
                quantity=random.randint(0,50),
                supplier_id=supplier.id,
                category_id=category.id,
            )
            session.add(new_product)
            session.commit()
    session.close()

    print("Products import complete.")




