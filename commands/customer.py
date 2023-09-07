import click
from models.models import *


@click.group(name='customer', help='--Customer management commands')
def customer_management_group():
    pass

@customer_management_group.command()
@click.option('--first_name', '-fn', prompt="First name")
@click.option('--last_name', '-ln', prompt="Last name")
def add_customer(first_name, last_name):
    customers = [customer.full_name.lower() for customer in session.query(Customer).all()]
    new_customer_fullname = f'{first_name.lower()} {last_name.lower()}'
    if new_customer_fullname not in customers:
        new_customer = Customer(
            first_name= first_name,
            last_name=last_name,
            full_name= f'{first_name} {last_name}'
        )
        session.add(new_customer)
        session.commit()
        click.echo(click.style("----------- CUSTOMER SUCCESSFULLY ADDED -----------", fg='green'))

    else:
        click.echo(click.style("Sorry! Customer already exists.", fg='red'))


