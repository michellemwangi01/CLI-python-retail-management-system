import click
from models.models import *
from commands.user_login import login

'''----------------------- P R O D U C T S -------------------------'''


@click.group(name='product', help='--Product management commands')
def product_management_group():
    pass


@product_management_group.command()
def view_category_products():
    """-View the all the products of specific category"""
    click.echo(click.style(f'{session.query(Category).all()}', fg='yellow'))
    category_id = click.prompt(
        click.style("Enter a number above to select the category", fg='cyan'), type=int)
    category_products = session.query(Product).join(Category.products).filter(
        Category.id == category_id).all()
    if category_products:
        click.echo(f"Products in category {session.query(Category).filter_by(id=category_id).first()} are:")
        for category_product in category_products:
            click.echo(click.style(f'{category_product}\n', fg='yellow'))
    else:
        click.echo(click.style("ERROR! No such product found.", fg='red', bold=True))


@product_management_group.command()
def view_supplier_products():
    """-View supplier products"""
    click.echo(click.style(f'{session.query(Supplier).all()}', fg='yellow'))
    supplier_id = click.prompt(
        click.style("Enter a number above to select the supplier", fg='cyan'), type=int)
    supplier_products = session.query(Product).join(Supplier.products).filter(
        Supplier.id == supplier_id).all()
    if supplier_products:
        click.echo(f"Products supplied by {session.query(Category).filter_by(id=supplier_id).first()} are:")
        for supplier_product in supplier_products:
            click.echo(click.style(f'{supplier_product}', fg='yellow'))
    else:
        click.echo(click.style("This supplier has no products or does not exist.", fg='red'))


@product_management_group.command()
@click.option('--name', '-pn', default=None, type=str, help="Search for a product by name")
def view_product_details(name):
    """-View product details"""
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
# @click.option('--name', '-n', prompt="Enter the product name", type=str)
# @click.option('--price', '-p', prompt="Enter the price", type=float)
# @click.option('--quantity', '-q', prompt="Enter the quantity", type=int)
def add_product():
    """-Add a new product"""
    new_product_name = click.prompt(click.style("Product name",fg='cyan'))
    new_product_price = click.prompt(click.style("Product price",fg='cyan'))
    new_product_quantity = click.prompt(click.style("Product quantity",fg='cyan'), type=int)
    click.echo(click.style(f'{session.query(Category).all()}', fg='yellow'))
    category_id = click.prompt(
        click.style("Enter a number above to select a category", fg='cyan'), type=int)
    click.echo(click.style(f'{session.query(Supplier).all()}', fg='yellow'))
    supplier_id = click.prompt(
        click.style("Enter a number above to select a supplier", fg='cyan'), type=int)
    category_record = session.query(Category).filter_by(id=category_id).first()
    supplier_record = session.query(Supplier).filter_by(id=supplier_id).first()
    stock_status = "In-stock" if new_product_quantity > 5 else "Reorder Required" if 0 < new_product_quantity < 5 else "Out of Stock"
    if category_record and supplier_record:
        new_product = Product(
            name=new_product_name,
            supplier_id=supplier_record.id,
            category_id=category_record.id,
            price=new_product_price,
            quantity=new_product_quantity,
            stock_status = stock_status
        )
        session.add(new_product)
        session.commit()
        click.echo(f'You have added the product: {new_product}')
        click.echo(click.style("------------- NEW PRODUCT ADDED SUCCESSFULLY -------------!", fg='green', bold=True))
    else:
        click.echo(click.style("Sorry! Category or Supplier you entered does not exist.", fg='red', bold=True))


@product_management_group.command()
def delete_product():
    """-Delete an existing product"""
    click.echo("Authorization required for this action.")
    current_user = login()
    if current_user and current_user.role == 'employee':
        search_name = click.prompt(click.style("Search for product to delete", fg='cyan'))
        product_to_delete = session.query(Product).filter(Product.name.like(f'%{search_name}%')).first()
        if product_to_delete:
            confirm_delete = click.prompt(click.style("Please note the the related purchases will also be deleted. Continue? Y/N", fg='cyan'))
            if confirm_delete.lower() =='y':
                session.delete(product_to_delete)
                session.commit()
                click.echo(
                    click.style("------------- PRODUCT HAS BEEN SUCCESSFULLY DELETED ------------", fg='green', bold=True))
            else:
                click.echo(click.style("Delete action aborted!", fg='red'))
        else:
            click.echo(click.style("Error! No such product exists.", fg='red', bold=True))
    else:
        click.echo(click.style("Sorry! Login failed or you are not authorized to perform this action"))

product_details = ("name", "price", "quantity", "category", "supplier")


@product_management_group.command()
@click.option('--choice', '-n', prompt="What would you like to update? Select", type=click.Choice(product_details))
@click.option('--name', '-n', prompt="What product would you like to update? (name)")
def update_product(choice, name):
    """-Update an existing product"""
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
