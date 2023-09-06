from models import *
import click


# _------------------------------ Create Command Groups ------------------------
@click.group()
def mycommands():
    pass


# @mycommandss.group(name='inventory', help="Inventory Management Commands")
# def inventory_group():
#     pass
#
#
# @mycommandss.group(name='customer', help="Customer Management Commands")
# def customer_group():
#     pass
#
#
# @mycommandss.group(name='supplier', help="Supplier Management Commands")
# def supplier_group():
#     pass
#
#
# @mycommandss.group(name='product', help="Product Management Commands")
# def product_group():
#     pass


categories = session.query(Category).all()
suppliers = session.query(Supplier).all()
products = session.query(Product).all()
# _------------------------------ Create Commands ------------------------

'''----------------------- C A T E G O R I E S ______________________--'''


@mycommands.command()
def view_categories():
    click.echo(session.query(Category).all())


@mycommands.command()
@click.option('--name', '-n', prompt="Enter the category name")
def new_category(name):
    if name not in categories:
        new_category = Category(
            name=name
        )
        session.add(new_category)
        session.commit()
        click.echo(f"Category '{name}' successfully added!")
    else:
        click.echo(f"Category '{name}' already exists.")


@mycommands.command()
@click.option('--search_name', '-sn', prompt="Enter the category name to update")
@click.option('--new_name', '-nn', prompt="Enter the name to be updated to")
def update_category(search_name, new_name):
    category_to_update = session.query(Category).filter(Category.name.like(f'%{search_name}%')).first()
    click.echo(f"{category_to_update}")
    if category_to_update:
        session.query(Category).filter_by(id=category_to_update.id).update({
            Category.name: f'C-{new_name}'
        })
        session.commit()
        click.echo("Name successfully updated!")
    else:
        click.echo("Sorry! That category does not exist and cannot be updated.")


@mycommands.command()
@click.option('--search_name', '-sn', prompt="Enter the category name to delete")
def delete_category(search_name):
    category_to_delete = session.query(Category).filter(Category.name.like(f'%{search_name}%')).first()
    click.echo(f"{category_to_delete}")
    if category_to_delete:
        session.delete(category_to_delete)
        session.commit()
        click.echo("Category successfully deleted!")
    else:
        click.echo("Sorry! That category does not exist and cannot be deleted.")


@mycommands.command()
@click.option('--category_name', '--cn', prompt="Enter the category to filter by")
def view_category_products(category_name):
    click.echo(
        session.query(Product).join(Category.products).filter(Category.name.like(f'%{category_name}%')).all())


'''----------------------- S U P P L I E R -------------------------'''


@mycommands.command()
def view_suppliers():
    click.echo(session.query(Supplier).all())


@mycommands.command()
@click.option('--name', '-n', prompt="Enter the supplier name")
def new_supplier(name):
    if name.lower() not in [supplier.name.lower() for supplier in suppliers]:
        new_supplier = Supplier(
            name=name
        )
        session.add(new_supplier)
        session.commit()
        click.echo(f"Supplier '{name}' successfully added!")
    else:
        click.echo(f"Supplier '{name}' already exists.")


@mycommands.command()
@click.option('--search_name', '-sn', prompt="Enter the supplier name to update")
@click.option('--new_name', '-nn', prompt="Enter the supplier name to update to")
def update_supplier(search_name, new_name):
    supplier_to_update = session.query(Supplier).filter(Supplier.name.like(f'%{search_name}%')).first()
    click.echo(f"{supplier_to_update}")
    if supplier_to_update:
        session.query(Supplier).filter_by(id=supplier_to_update.id).update({
            Supplier.name: f'C-{new_name}'
        })
        session.commit()
        click.echo("Supplier name successfully updated!")
    else:
        click.echo("Sorry! That supplier does not exist and cannot be updated.")


@mycommands.command()
@click.option('--search_name', '-sn', prompt="Enter the category name to delete")
def delete_supplier(search_name):
    supplier_to_delete = session.query(Supplier).filter(Supplier.name.like(f'%{search_name}%')).first()
    click.echo(f"{supplier_to_delete}")
    if supplier_to_delete:
        session.delete(supplier_to_delete)
        session.commit()
        click.echo("Supplier successfully deleted!")
    else:
        click.echo("Sorry! That supplier does not exist and cannot be deleted.")


@mycommands.command()
@click.option('--search_supplier', '-ssup', prompt="Enter name of the supplier to see related products")
def view_supplier_products(search_supplier):
    click.echo(
        session.query(Product).join(Product.supplier).filter(Supplier.name.like(f'%{search_supplier}%')).all())


'''----------------------- P R O D U C T S -------------------------'''


@mycommands.command()
@click.option('--name', '-pn', default=None, type=str, help="Search for a product by name")
def view_product_details(name):
    if name is None:
        for product in session.query(Product):
            click.echo(
                f'({product.id}): Name:{product.name}, Price:{product.price} | Quantity:{product.quantity} | Category:{product.category.name} | Product:{product.supplier.name}')
    else:
        product = session.query(Product).filter(Product.name.like(f'%{name}%')).first()
        if product:
            click.echo(
                f'({product.id}): Name:{product.name}, Price:{product.price} | Quantity:{product.quantity} | Category:{product.category.name} | Product:{product.supplier.name}')
        else:
            click.echo("Product you searched fo does not exist.")


@mycommands.command()
@click.option('--name', '-n', prompt="Enter the product name", type=str)
@click.option('--category', '-c', prompt="Enter the category", type=str)
@click.option('--supplier', '-s', prompt="Enter the supplier name", type=str)
@click.option('--price', '-p', prompt="Enter the price", type=float)
@click.option('--quantity', '-q', prompt="Enter the quantity", type=int)
def add_product(name, category, supplier, price, quantity):
    category_record = session.query(Category).filter(Category.name.like(f'%{category}%')).first()
    supplier_record = session.query(Supplier).filter(Supplier.name.like(f'%{supplier}%')).first()
    click.echo(category_record)
    click.echo(supplier_record)
    if category_record and supplier_record:
        new_product = Product(
            name=f'P-{name}',
            supplier_id=supplier_record.id,
            category_id=category_record.id,
            price=price,
            quantity=quantity,
        )
        session.add(new_product)
        session.commit()
        click.echo("New product added successfully!")
    else:
        click.echo("Sorry! Category or Supplier you entered does not exist.")


@mycommands.command()
@click.option('--name', '-n', help="Search for product to delete", prompt="Enter product name to be deleted")
def delete_product(name):
    product_to_delete = session.query(Product).filter(Product.name.like(f'%{name}%')).first()
    if product_to_delete:
        session.delete(product_to_delete)
        session.commit()
        click.echo("Product has been successfully deleted")
    else:
        click.echo("Error! No such product exists.")


product_details = ("name","price", "quantity", "category","supplier")
table_options = {
    "products": Product,
    "categories": Category,
    "suppliers": Supplier,
    "customers": Customer,
    "purchases": Purchase
}


@mycommands.command()
@click.option('--choice', '-n', prompt="What would you like to update? Select", type=click.Choice(product_details))
@click.option('--name', '-n', prompt="What product would you like to update? (name)")
def update_product(choice, name):
    product_to_update = session.query(Product).filter(Product.name.like(f'%{name}%')).first()
    update_data = {}
    if product_to_update:
        click.echo(f"{product_to_update}")
        if choice.lower() == 'name':
            new_name = click.prompt("Enter the new name")
            update_data['name'] = f'P-{new_name}'
        if choice.lower() == 'price':
            new_price = click.prompt("Enter the new price")
            update_data['price'] = new_price
        if choice.lower() == 'quantity':
            new_quantity = click.prompt("Enter the new quantity")
            update_data['quantity'] = new_quantity

        # update foreign key values
        if choice.lower() == 'supplier':
            update_to_supplier = click.prompt("Enter the new supplier")
            supplier_record = session.query(Supplier).filter(Supplier.name.like(f'%{update_to_supplier}%')).first()
            if supplier_record:
                update_data['supplier_id'] = supplier_record.id
            else:
                click.echo(
                    "Entered supplier does not exist. View existing products using the 'view-suppliers' command.")
        if choice.lower() == 'category':
            update_to_category = click.prompt("Enter the new category")
            category_record = session.query(Category).filter(Category.name.like(f'%{update_to_category}%')).first()
            if category_record:
                update_data['category_id'] = category_record.id
            else:
                click.echo(
                    "Entered category does not exist. View existing categories using the 'view-categories' command.")
        print(update_data)
        session.query(Product).filter_by(id=product_to_update.id).update(update_data)
        session.commit()
        click.echo("Product is successfully updated!")
    else:
        click.echo(
            "Sorry! That product does not exist and cannot be updated. View existing products using the 'view-product-details' command.")


@mycommands.command()
@click.option('--customer_name', '-cn', prompt="Customer purchasing the product? (name)")
@click.option('--product_name', '-pn', prompt="Product to be purchased? (name)")
@click.option('--quantity', '-pn', type=int, prompt="Quantity purchased?")
def add_purchase(customer_name, product_name, quantity):
    customer = session.query(Customer).filter(Customer.full_name.like(f'%{customer_name}%')).first()
    product = session.query(Product).filter(Product.name.like(f'%{product_name}%')).first()

    if customer and product:
        existing_purchase = session.query(Purchase).filter(and_(
                Purchase.customer_id == customer.id,
                Purchase.product_id == product.id
            )
        ).first()
        print(f'existing_purchase: {existing_purchase}')
        if existing_purchase:
            session.query(Purchase).filter(
                Purchase.customer_id == customer.id,
                Purchase.product_id == product.id
            ).update({
                Purchase.quantity: Purchase.quantity+quantity
            })
            session.commit()
            click.echo("This purchase already exists in the database. \n"
                       "------------ QUANTITY SUCCESSFULLY UPDATED ----------- ")
        else:
            new_purchase = Purchase(
                customer_id=customer.id,
                product_id=product.id,
                quantity=quantity
            )
            session.add(new_purchase)
            product_to_update = session.query(Product).filter(Product.id==product.id).first()
            print(f'product_to_update: {product_to_update.quantity}')
            if product_to_update.quantity > quantity:
                session.query(Product).filter(Product.id==product.id).update({
                    Product.quantity: Product.quantity - quantity
                })
                session.commit()
            else:
                click.echo(f"-------------- ERROR ------------\n"
                           f"Only {product.quantity} remaining to be purchased!")

            session.commit()
            click.echo("----------- PURCHASE SUCCESSFULLY ADDED ------------")
    else:
        click.echo("ERROR! Product or Customer you entered does not exist")


purchase_details = ("customer","product", "quantity")

@mycommands.command()
@click.option('--choice', '-n', prompt="What column would you like to update? Select", type=click.Choice(purchase_details))
@click.option('--name', '-n', prompt="Which purchase record would you like to update? (name)")
def update_purchase(choice, name):
    purchase_to_update = session.query(Purchase).filter(Purchase.customer.name.like(f'%{name}%')).first()
    print(purchase_to_update)
    update_data = {}
    if purchase_to_update:
        click.echo(f"{purchase_to_update}")
        if choice.lower() == 'quantity':
            new_quantity = click.prompt("Enter the new quantity")
            update_data['quantity'] = new_quantity

        # update foreign key values
        if choice.lower() == 'customer':
            update_to_customer = click.prompt("Enter the new customer name")
            customer_record = session.query(Supplier).filter(Supplier.name.like(f'%{update_to_customer}%')).first()
            if customer_record:
                update_data['customer_id'] = customer_record.id
            else:
                click.echo(
                    "Entered customer does not exist. View existing purchases using the 'view-purchases' command.")
        if choice.lower() == 'product':
            update_to_product = click.prompt("Enter the new product name")
            product_record = session.query(Category).filter(Category.name.like(f'%{update_to_product}%')).first()
            if product_record:
                update_data['product_id'] = product_record.id
            else:
                click.echo(
                    "Entered product does not exist. View existing products using the 'view-products' command.")
        print(update_data)
        session.query(Product).filter_by(id=purchase_to_update.id).update(update_data)
        session.commit()
        click.echo("Purchase is successfully updated!")
    else:
        click.echo(
            "Sorry! That purchase record does not exist and cannot be updated. View existing purchases using the 'view-purchase-details' command.")





































# @mycommands.command()
# @click.option('--choice', '-n', prompt="Table to delete from? Select", type=click.Choice(table_options))
# @click.option('--name', '-n', prompt="Record from the table to delete (name)")
# def delete_records(choice, name):
#     print(choice, name)
#     record_to_delete = session.query(table_options[choice]).filter(table_options[choice].name.like(f'%{name.title()}%')).first()
#     print(record_to_delete)
#     if record_to_delete:
#         session.delete(record_to_delete)
#         session.commit()
#         click.echo("Product has been successfully deleted")
#     else:
#         click.echo("Error! No such product exists.")


if __name__ == '__main__':
    # Invoke mycommandss() method which calls all the commands
    mycommands()
