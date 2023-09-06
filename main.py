import random

from models import *
import click


# _------------------------------ Create Command Groups ------------------------
@click.group()
def mycommands():
    pass

'''----------------------- C A T E G O R I E S ______________________--'''


@mycommands.command()
def view_categories():
    click.echo(session.query(Category).all())


@mycommands.command()
@click.option('--name', '-n', prompt="Enter the category name")
def new_category(name):
    categories = session.query(Category)
    if name not in categories:
        new_category = Category(
            name=name
        )
        session.add(new_category)
        session.commit()
        click.echo(click.style(f"--------------- CATEGORY SUCCESSFULLY ADDED ----------------", fg='green', bold=True))
    else:
        click.echo(click.style(f"*** Category '{name}' already exists. ***", fg='red'))


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
        click.echo(click.style("-------------- NAME SUCCESSFULLY UPDATED -------------", fg='green',bold=True ))
    else:
        click.echo(click.style(" *** Sorry! That category does not exist and cannot be updated. ***", fg='red', bold=True))


@mycommands.command()
@click.option('--search_name', '-sn', prompt="Enter the category name to delete")
def delete_category(search_name):
    category_to_delete = session.query(Category).filter(Category.name.like(f'%{search_name}%')).first()
    if category_to_delete:
        confirmation = click.prompt(
            "To complete delete, related product records will be updated to a different supplier via auto-assign or selected supplier. Continue? Y/N")
        if confirmation.lower() == 'y':
            category_update_mode = click.prompt(
                "Update via auto-assign or selected supplier? Enter 1 or 2 to choose.\n1. Auto-assign (1)\n2. Select Category(2)\nEnter Selection",
                type=int)
            if category_update_mode == 1:
                products_to_update_category = session.query(Product).filter(
                    Product.category_id == category_to_delete.id).all()
                if products_to_update_category:
                    categories = session.query(Category).filter(Category.id != category_to_delete.id).all()
                    random_category = random.choice(categories)
                    session.query(Product).filter(Product.category_id == category_to_delete.id).update(
                        {
                            Product.category_id: random_category.id
                        }
                    )
                    click.echo(click.style(f"Product categories successfully updated to {random_category}", fg='green',
                                           bold=True))
                    session.delete(category_to_delete)
                    session.commit()
                    click.echo(click.style("------------------- CATEGORY SUCCESSFULLY DELETED ---------------------",
                                           fg='green', bold=True))
                else:
                    click.echo(click.style("No related products found!",fg='red', bold=True))
            elif category_update_mode == 2:
                new_category_name = click.prompt(click.style("Which category would you like to transfer the product records to?",fg='cyan', bold=True))
                new_category = session.query(Category).filter(Category.name.like(f'%{new_category_name}%')).first()
                session.query(Product).filter(Product.supplier_id == category_to_delete.id).update(
                    {
                        Product.category_id: new_category.id
                    }
                )
                click.echo(
                    click.style(f"Product categories successfully updated to {new_category}!", fg='green', bold=True))
                session.delete(category_to_delete)
                session.commit()
                click.echo(
                    click.style("------------------- CATEGORY SUCCESSFULLY DELETED ---------------------", fg='green',
                                bold=True))
            else:
                click.echo(click.style("ERROR! Input Invalid", fg='red', bold=True))
        elif confirmation.lower() == 'n':
            click.echo(click.style("Delete Action Aborted!", fg='red', bold=True))
        else:
            click.echo(click.style("ERROR! Invalid input!", fg='red', bold=True))
    else:
        click.echo(click.style("ERROR! That category does not exist and cannot be deleted.", fg='red', bold=True))


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
    suppliers = session.query(Supplier)
    if name.lower() not in [supplier.name.lower() for supplier in suppliers]:
        new_supplier = Supplier(
            name=name
        )
        session.add(new_supplier)
        session.commit()
        click.echo(click.style(f"---------------- SUPPLIER '{name}' SUCCESSFULLY ADDED ---------------", fg='green', bold=True))
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


@mycommands.command('')
@click.option('--search_name', '-sn', prompt="Enter the supplier name to delete")
def delete_supplier(search_name):
    supplier_to_delete = session.query(Supplier).filter(Supplier.name.like(f'%{search_name}%')).first()
    if supplier_to_delete:
        confirmation = click.prompt("To complete delete, related product records will be updated to a different supplier via auto-assign or selected supplier. Continue? Y/N")
        if confirmation.lower() == 'y':
            supplier_update_mode = click.prompt("Update via auto-assign or selected supplier? Enter 1 or 2 to choose.\n1. Auto-assign (1)\n2. Select Supplier(2)\nEnter Selection", type=int)
            if supplier_update_mode == 1:
                products_to_update_supplier = session.query(Product).filter(Product.supplier_id == supplier_to_delete.id).all()
                if products_to_update_supplier:
                    suppliers = session.query(Supplier).filter(Supplier.id != supplier_to_delete.id).all()
                    random_supplier = random.choice(suppliers)
                    session.query(Product).filter(Product.supplier_id == supplier_to_delete.id).update(
                        {
                            Product.supplier_id: random_supplier.id
                        }
                    )
                    click.echo(click.style(f"Product Suppliers successfully updated to {random_supplier}!", fg='green',bold=True))
                    session.delete(supplier_to_delete)
                    session.commit()
                    click.echo(click.style("------------------- SUPPLIER SUCCESSFULLY DELETED ---------------------",
                                           fg='green', bold=True))
                else:
                    click.echo("No related products found!")
            elif supplier_update_mode == 2:
                new_supplier_name = click.prompt("Which supplier would you like to transfer the product records to?")
                new_supplier = session.query(Supplier).filter(Supplier.name.like(f'%{new_supplier_name}%')).first()
                session.query(Product).filter(Product.supplier_id == supplier_to_delete.id).update(
                    {
                        Product.supplier_id: new_supplier.id
                    }
                )
                click.echo(click.style(f"Product Suppliers successfully updated to {new_supplier}!", fg='red', bold=True))
                session.delete(supplier_to_delete)
                session.commit()
                click.echo(click.style("------------------- SUPPLIER SUCCESSFULLY DELETED ---------------------", fg='green', bold=True))
            else:
                click.command(click.style("ERROR! Input Invalid", fg='red', bold=True))
        elif confirmation.lower() == 'n':
            click.echo(click.style("--------------- Delete Action Aborted ----------------",fg='red', bold=True))
        else:
            click.echo(click.style("ERROR! Invalid input!", fg='red', bold=True))
    else:
        click.echo(click.style("Sorry! That supplier does not exist and cannot be deleted.", fg='red', bold=True))


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
            click.echo(click.style("Product you searched for does not exist.", fg='red', bold=True))


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
        click.echo(click.style("------------- NEW PRODUCT ADDED SUCCESSFULLY -------------!", fg='green', bold=True))
    else:
        click.echo(click.style("Sorry! Category or Supplier you entered does not exist.",fg='green', bold=True))


@mycommands.command()
@click.option('--name', '-n', help="Search for product to delete", prompt="Enter product name to be deleted")
def delete_product(name):
    product_to_delete = session.query(Product).filter(Product.name.like(f'%{name}%')).first()
    if product_to_delete:
        session.delete(product_to_delete)
        session.commit()
        click.echo(click.style("------------- PRODUCT HAS BEEN SUCCESSFULLY DELETED ------------", fg='green', bold=True))
    else:
        click.echo(click.style("Error! No such product exists.", fg='green', bold=True))


product_details = ("name", "price", "quantity", "category", "supplier")

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
                    click.style("Entered supplier does not exist. View existing products using the 'view-suppliers' command.", fg='red', bold=True))
        if choice.lower() == 'category':
            update_to_category = click.prompt("Enter the new category")
            category_record = session.query(Category).filter(Category.name.like(f'%{update_to_category}%')).first()
            if category_record:
                update_data['category_id'] = category_record.id
            else:
                click.echo(
                    click.style("Entered category does not exist. View existing categories using the 'view-categories' command.", fg='red', bold=True))
        print(update_data)
        session.query(Product).filter_by(id=product_to_update.id).update(update_data)
        session.commit()
        click.echo(click.style("----------- PRODUCT IS SUCCESSFULLY UPDATED --------------", bg='green', bold=True))
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
        # existing_purchase = session.query(Purchase).filter(and_(
        #         Purchase.customer_id == customer.id,
        #         Purchase.product_id == product.id
        #     )
        # ).first()
        # print(f'existing_purchase: {existing_purchase}')
        # if existing_purchase:
        #     session.query(Purchase).filter(
        #         Purchase.customer_id == customer.id,
        #         Purchase.product_id == product.id
        #     ).update({
        #         Purchase.quantity: Purchase.quantity+quantity
        #     })
        #     session.commit()
        #     click.echo("This purchase already exists in the database. \n"
        #                "------------ QUANTITY SUCCESSFULLY UPDATED ----------- ")
        # else:
        new_purchase = Purchase(
            customer_id=customer.id,
            product_id=product.id,
            quantity=quantity
        )
        session.add(new_purchase)
        product_to_update = session.query(Product).filter(Product.id == product.id).first()
        if product_to_update.quantity > quantity:
            session.query(Product).filter(Product.id == product.id).update({
                Product.quantity: Product.quantity - quantity
            })
            session.commit()
        else:
            click.echo(click.style(f"ERROR! Unable to purchase. Only {product.quantity} item remaining to be purchased!", fg='red',bold=True))

        session.commit()
        click.echo(click.style("----------- PURCHASE SUCCESSFULLY ADDED ------------", fg='green', bold=True))
    else:
        click.echo(click.style("ERROR! Product or Customer you entered does not exist", fg='red', bold=True))


@mycommands.command()
@click.option('--name', '-f', prompt="Name of customer")
def view_customer_purchase_details(name):
    customer = session.query(Customer).filter(Customer.full_name.like(f'%{name}%')).first()
    if customer:
        for purchase in customer.purchases:
            click.echo(f'({purchase.id}) Customer: {purchase.customer.full_name} | Product: {purchase.product.name} | Qty: {purchase.quantity}\n')
    else:
        click.echo(click.style("ERROR! Entered customer was not found.", fg='red', bold=True))


@mycommands.command()
@click.option('--name', '-f', prompt="Name of product")
def view_product_purchase_details(name):
    product = session.query(Product).filter(Product.name.like(f'%{name}%')).first()
    if product:
        for purchase in product.purchases:
            click.echo(f'({purchase.id}) Customer: {purchase.customer.full_name} | Product: {purchase.product.name} | Qty: {purchase.quantity}\n')
    else:
        click.echo(click.style("ERROR! Entered product was not found.", fg='green', bold=True))


if __name__ == '__main__':
    # Invoke mycommands() method which calls all the commands
    mycommands()
