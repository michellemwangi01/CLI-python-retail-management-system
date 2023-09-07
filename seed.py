from configuration.imports import *
from models.models import *
from faker import Faker
import random

fake = Faker()

categories = ["Fresh Produce", "Dairy Products", "Bakery Items", "Meat and Poultry", "Seafood", "Canned Goods",
              "Frozen Foods", "Snack Foods", "Beverages", "Condiments and Sauces"]
categories2 = ["Cereal and Breakfast Foods",
              "Pasta and Rice", "Canned and Dried Beans", "Personal Care Products", "Cleaning Supplies",
              "Paper Products",
              "Health and Wellness", "Pet Supplies", "Household Goods", "Baby Care Products"]
suppliers = ["GreenGrocer Suppliers", "FreshHarvest Foods", "QualityProvisions Co.", "PantryMaster Distributors",
             "FarmToTable Supplies", "Gourmet Essentials Ltd.", "PrimeGrocery Suppliers", "MegaMart Wholesalers",
             "EpicProduce Distributors", "PremiumPantry Imports"]

if __name__ == '__main__':

    session.query(Product).delete()
    session.query(Supplier).delete()
    session.query(Category).delete()
    session.query(Purchase).delete()
    session.query(Customer).delete()

    '''----------------------- C A T E G O R I E S ______________________--'''
    for item in categories:
        new_category = Category(
            name=f'{item}'
        )
        session.add(new_category)
        session.commit()
    print("Category import complete.")

    '''----------------------- S U P P L I E R S ______________________--'''
    for item in suppliers:
        new_supplier = Supplier(
            name=f'{item}'
        )
        session.add(new_supplier)
        session.commit()
    print("Supplier import complete.")

    '''----------------------- P R O D U C T S ______________________--'''
    products = []
    for item in categories:
        for i in range(random.randint(1, 10)):
            supplier = session.query(Supplier).order_by(func.random()).first()
            category = session.query(Category).order_by(func.random()).first()
            new_product = Product(
                name=f'{fake.name()}',
                price=round(random.uniform(100, 1000), 2),
                quantity=random.randint(0, 50),
                supplier_id=supplier.id,
                category_id=category.id,
            )
            session.add(new_product)
            session.commit()
            products.append(new_product)
    session.close()

    print("Products import complete.")

    '''----------------------- C U S T O M E R ______________________--'''
    customers = []
    for num in range(1, 20):
        first_name = fake.first_name()
        last_name = fake.last_name()
        new_customer = Customer(
            first_name=first_name,
            last_name=last_name,
            full_name=f'{first_name} {last_name}'
        )
        session.add(new_customer)
        session.commit()
        customers.append(new_customer)
    print("Customer import complete.")

    '''----------------------- P U R C H A S E S ______________________--'''
    purchases = []
    for customer in customers:
        product = session.query(Product).order_by(func.random()).first()
        for i in range(random.randint(1, 4)):
            new_purchase = Purchase(
                customer_id=customer.id,
                product_id=product.id,
                quantity=random.randint(2, 6)
            )
            session.add(new_purchase)
            session.commit()
            purchases.append(new_purchase)
    print("Purchases import complete.")

