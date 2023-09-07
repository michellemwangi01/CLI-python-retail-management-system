import click
from models.models import *


'''----------------------- P R O D U C T S -------------------------'''


@click.group(name='product', help='--Product management commands')
def product_management_group():
    pass


@product_management_group.command()
@click.option('--category_name', '--cn', prompt="Enter the category to filter by")
def view_category_products(category_name):
    '''View the all the products of specific category'''
    category_products = session.query(Product).join(Category.products).filter(
        Category.name.like(f'%{category_name}%')).all()
    if category_products:
        for category_product in category_products:
            click.echo(click.style(f'{category_product}\n', fg='yellow'))
    else:
        click.echo(click.style("ERROR! No such product found.", fg='red', bold=True))


@product_management_group.command()
@click.option('--search_supplier', '-ssup', prompt="Enter name of the supplier to see related products")
def view_supplier_products(search_supplier):
    '''View supplier products'''
    supplier_products = session.query(Product).join(Product.supplier).filter(
        Supplier.name.like(f'%{search_supplier}%')).all()
    if supplier_products:
        for supplier_product in supplier_products:
            click.echo(click.style(f'{supplier_product}', fg='yellow'))
    else:
        click.echo(click.style("This supplier has not products or does not exist.", fg='red'))


@product_management_group.command()
@click.option('--name', '-pn', default=None, type=str, help="Search for a product by name")
def view_product_details(name):
    '''View product details'''
    if name is None:
        for product in session.query(Product):
            click.echo(click.style(
                f'({product.id}): Name:{product.name}, Price:{product.price} | Quantity:{product.quantity} | Category:{product.category.name} | Product:{product.supplier.name}',
                fg='yellow')
            )
    else:
        product = session.query(Product).filter(Product.name.like(f'%{name}%')).first()
        if product:
            click.echo(click.style(
                f'({product.id}): Name:{product.name}, Price:{product.price} | Quantity:{product.quantity} | Category:{product.category.name} | Product:{product.supplier.name}',
                fg='yellow')
            )
        else:
            click.echo(click.style("Product you searched for does not exist.", fg='red', bold=True))


@product_management_group.command()
@click.option('--name', '-n', prompt="Enter the product name", type=str)
@click.option('--category', '-c', prompt="Enter the category", type=str)
@click.option('--supplier', '-s', prompt="Enter the supplier name", type=str)
@click.option('--price', '-p', prompt="Enter the price", type=float)
@click.option('--quantity', '-q', prompt="Enter the quantity", type=int)
def add_product(name, category, supplier, price, quantity):
    '''Add a new product'''
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
        click.echo(click.style("Sorry! Category or Supplier you entered does not exist.", fg='red', bold=True))


@product_management_group.command()
@click.option('--name', '-n', help="Search for product to delete", prompt="Enter product name to be deleted")
def delete_product(name):
    '''delete an existing product'''
    product_to_delete = session.query(Product).filter(Product.name.like(f'%{name}%')).first()
    if product_to_delete:
        session.delete(product_to_delete)
        session.commit()
        click.echo(
            click.style("------------- PRODUCT HAS BEEN SUCCESSFULLY DELETED ------------", fg='green', bold=True))
    else:
        click.echo(click.style("Error! No such product exists.", fg='red', bold=True))


product_details = ("name", "price", "quantity", "category", "supplier")


@product_management_group.command()
@click.option('--choice', '-n', prompt="What would you like to update? Select", type=click.Choice(product_details))
@click.option('--name', '-n', prompt="What product would you like to update? (name)")
def update_product(choice, name):
    '''Update an existing product'''
    product_to_update = session.query(Product).filter(Product.name.like(f'%{name}%')).first()
    update_data = {}
    if product_to_update:
        click.echo(f"{product_to_update}")
        if choice.lower() == 'name':
            new_name = click.prompt(click.style("Enter the new name", fg='cyan'))
            update_data['name'] = f'P-{new_name}'
        if choice.lower() == 'price':
            new_price = click.prompt(click.style("Enter the new price", fg='cyan'))
            update_data['price'] = new_price
        if choice.lower() == 'quantity':
            new_quantity = click.prompt(click.style("Enter the new quantity", fg='cyan'))
            update_data['quantity'] = new_quantity

        # update foreign key values
        if choice.lower() == 'supplier':
            update_to_supplier = click.prompt(click.style("Enter the new supplier", fg='cyan'))
            supplier_record = session.query(Supplier).filter(Supplier.name.like(f'%{update_to_supplier}%')).first()
            if supplier_record:
                update_data['supplier_id'] = supplier_record.id
            else:
                click.echo(
                    click.style(
                        "Error! Entered supplier does not exist. View existing products using the 'view-suppliers' command.",
                        fg='red', bold=True))
        if choice.lower() == 'category':
            update_to_category = click.prompt(click.style("Enter the new category", fg='cyan'))
            category_record = session.query(Category).filter(Category.name.like(f'%{update_to_category}%')).first()
            if category_record:
                update_data['category_id'] = category_record.id
            else:
                click.echo(
                    click.style(
                        "ERROR! Entered category does not exist. View existing categories using the 'view-categories' command.",
                        fg='red', bold=True))
        print(update_data)
        session.query(Product).filter_by(id=product_to_update.id).update(update_data)
        session.commit()
        click.echo(click.style("----------- PRODUCT IS SUCCESSFULLY UPDATED --------------", bg='green', bold=True))
    else:
        click.echo(click.style(
            "ERROR! That product does not exist and cannot be updated. View existing products using the 'view-product-details' command.",
            fg='red', bold=True)
        )