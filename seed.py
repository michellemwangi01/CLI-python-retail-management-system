from configuration.imports import *
from models.models import *
from faker import Faker
import random

fake = Faker()

categories = ("Fresh Produce", "Dairy Products", "Bakery Items", "Meat and Poultry", "Seafood", "Canned Goods",
              "Frozen Foods", "Snack Foods", "Beverages", "Condiments and Sauces")
categories2 = ("Cereal and Breakfast Foods",
               "Pasta and Rice", "Canned and Dried Beans", "Personal Care Products", "Cleaning Supplies",
               "Paper Products",
               "Health and Wellness", "Pet Supplies", "Household Goods", "Baby Care Products")
suppliers = ("GreenGrocer Suppliers", "FreshHarvest Foods", "QualityProvisions Co.", "PantryMaster Distributors",
             "FarmToTable Supplies", "Gourmet Essentials Ltd.", "PrimeGrocery Suppliers", "MegaMart Wholesalers",
             "EpicProduce Distributors", "PremiumPantry Imports")
user_roles = ('Employee', 'Customer')
sample_products = ("Bread",
    "Milk",
    "Eggs",
    "Fresh Vegetables (e.g., lettuce, tomatoes, carrots)",
    "Fresh Fruits (e.g., apples, bananas, oranges)",
    "Rice",
    "Pasta",
    "Canned Soup",
    "Cereal",
    "Cheese",
    "Yogurt",
    "Ground Beef",
    "Chicken Breast",
    "Pork Chops",
    "Butter",
    "Frozen Pizza",
    "Canned Tuna",
    "Peanut Butter",
    "Jelly or Jam",
    "Breakfast Cereal",
    "Bottled Water",
    "Soft Drinks",
    "Snack Chips",
    "Laundry Detergent",
    "Toilet Paper")

if __name__ == '__main__':

    session.query(Product).delete()
    session.query(Supplier).delete()
    session.query(Category).delete()
    session.query(Purchase).delete()
    session.query(Customer).delete()
    session.query(User).delete()

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
    for item in sample_products:
        supplier = session.query(Supplier).order_by(func.random()).first()
        category = session.query(Category).order_by(func.random()).first()
        new_product = Product(
            name=item,
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
            full_name=f'{first_name} {last_name}',
            loyalty_points=0
        )
        session.add(new_customer)
        session.commit()
        new_user = User(
            username=f'{new_customer.first_name}.{new_customer.last_name}',
            password=fake.unique.word(),
            role=random.choice(['customer', 'employee']),
            customer_id=new_customer.id
        )
        session.add(new_user)
        session.commit()
        customers.append(new_user)
        customers.append(new_customer)
    print("Customer import complete.")
    print("User import complete.")

    '''----------------------- P U R C H A S E S ______________________--'''
    purchases = []
    for customer in customers:
        product = session.query(Product).order_by(func.random()).first()
        quantity = random.randint(2, 6)
        for i in range(random.randint(1, 4)):
            new_purchase = Purchase(
                customer_id=customer.id,
                product_id=product.id,
                quantity= quantity,
                total_amount = product.price * quantity
            )
            session.add(new_purchase)
            session.commit()
            purchases.append(new_purchase)
    print("Purchases import complete.")

    '''----------------------- U S E R S ______________________--'''
    # users = []
    # for num in range(1, 5):
    #     username = f'{fake.first_name()}.{fake.first_name()}'
    #     new_user = User(
    #         username = f'{fake.first_name()}.{fake.first_name()}',
    #         password= fake.unique.word(),
    #         role= 'Employee'
    #
    #     )
    #     session.add(new_user)
    #     session.commit()
    #     customers.append(new_user)
    # print("User import complete.")
