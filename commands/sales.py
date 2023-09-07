import click
from models.models import *

'''----------------------- S A L E S ______________________--'''
@click.group(name='sales', help='--Sales management commands')
def sales_management_group():
    pass


@sales_management_group.command()
@click.option('--customer_name', '-cn', prompt="Customer purchasing the product? (name)")
@click.option('--product_name', '-pn', prompt="Product to be purchased? (name)")
@click.option('--quantity', '-pn', type=int, prompt="Quantity purchased?")
def add_purchase(customer_name, product_name, quantity):
    """-Add a new purchase"""
    click.prompt(click.style("Search for a customer"))
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
        #     click.echo("This purchase already exists in the configuration. \n"
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
            click.echo(
                click.style(f"ERROR! Unable to purchase. Only {product.quantity} item remaining to be purchased!",
                            fg='red', bold=True))

        session.commit()
        click.echo(click.style("----------- PURCHASE SUCCESSFULLY ADDED ------------", fg='green', bold=True))
    else:
        click.echo(click.style("ERROR! Product or Customer you entered does not exist", fg='red', bold=True))

@sales_management_group.command()
@click.option('--name', '-f', prompt="Name of customer")
def customer_purchase_history(name):
    '''View customer purchases'''
    customer = session.query(Customer).filter(Customer.full_name.like(f'%{name}%')).first()
    if customer:
        for purchase in customer.purchases:
            click.echo(
               click.style( f'({purchase.id}) Customer: {purchase.customer.full_name} | Product: {purchase.product.name} | Qty: {purchase.quantity} | {purchase.purchase_date}\n',fg='yellow'))
    else:
        click.echo(click.style("ERROR! Entered customer was not found.", fg='red', bold=True))

@sales_management_group.command()
@click.option('--name', '-f', prompt="Name of product")
def view_product_purchase_details(name):
    '''View product purchases'''
    product = session.query(Product).filter(Product.name.like(f'%{name}%')).first()
    if product:
        for purchase in product.purchases:
            click.echo(
                f'({purchase.id}) Customer: {purchase.customer.full_name} | Product: {purchase.product.name} | Qty: {purchase.quantity}\n')
    else:
        click.echo(click.style("ERROR! Entered product was not found.", fg='green', bold=True))
