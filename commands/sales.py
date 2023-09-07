import click
from models.models import *
from commands.user_login import login

'''----------------------- S A L E S ______________________--'''


@click.group(name='sales', help='--Sales management commands')
def sales_management_group():
    pass


@sales_management_group.command()
def make_purchase():
    """-Add a new purchase"""
    click.echo(click.style("Login to make a purchase"))
    current_user = login()
    if current_user:
        product_search = click.prompt(click.style("Product to purchase", fg='cyan'))
        product_to_purchase = session.query(Product).filter(Product.name.like(f'%{product_search}%')).first()
        quantity = click.prompt(click.style("Quantity to purchase", fg='cyan'), type=int)
        if product_to_purchase:
            print(product_to_purchase)
            if product_to_purchase.quantity > quantity:
                session.query(Product).filter_by(id=product_to_purchase.id).update({
                    Product.quantity: Product.quantity - quantity
                })
                session.commit()
                new_purchase = Purchase(
                    customer_id=current_user.customer_id,
                    product_id=product_to_purchase.id,
                    quantity=quantity,
                    total_amount=product_to_purchase.price * quantity
                )
                session.add(new_purchase)
                session.commit()
                click.echo(click.style(
                    f'--Purchase details--\nPurchased by: {current_user.username}\nProduct: {product_to_purchase.name}\nQty: {quantity}\nTotal Amount: {new_purchase.total_amount}\nDate of Purchase: {new_purchase.purchase_date}'))
                click.echo(click.style("----------- PURCHASE SUCCESSFULL ------------", fg='green', bold=True))
                click.echo(current_user)
                # update customer loyalty points
                customer_to_update_points = session.query(Customer).filter_by(id=current_user.customer_id).first()
                if customer_to_update_points:
                    calculated_points = new_purchase.total_amount % 100
                    customer_to_update_points.loyalty_points += round(calculated_points)
                    session.commit()
            else:
                click.echo(
                    click.style(f"Unable to purchase. Only {product_to_purchase.quantity} items remaining in stock!",
                                fg='red'))
        else:
            click.echo(click.style("ERROR! Product you entered does not exist", fg='red'))
    else:
        return


@sales_management_group.command()
@click.option('--name', '-f', prompt="Name of customer")
def customer_purchase_history(name):
    '''View customer purchases'''
    customer = session.query(Customer).filter(Customer.full_name.like(f'%{name}%')).first()
    if customer:
        for purchase in customer.purchases:
            click.echo(
                click.style(
                    f'({purchase.id}) Customer: {purchase.customer.full_name} | Product: {purchase.product.name} | Qty: {purchase.quantity} | {purchase.purchase_date}\n',
                    fg='yellow'))
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
