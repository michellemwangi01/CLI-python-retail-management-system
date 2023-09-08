import click

from models.models import *
from commands.user_login import login


@click.group(name='customer', help='--Customer management commands')
def customer_management_group():
    pass


@customer_management_group.command()
@click.option('--first_name', '-fn', prompt="First name")
@click.option('--last_name', '-ln', prompt="Last name")
def add_customer(first_name, last_name):
    """-Add a new customer to customer table"""
    customers = [customer.full_name.lower() for customer in session.query(Customer).all()]
    new_customer_fullname = f'{first_name.lower()} {last_name.lower()}'
    if new_customer_fullname not in customers:
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
            role='customer',
            password='password',
            customer_id=new_customer.id
        )
        session.add(new_user)
        session.commit()
        click.echo(click.style(f'New customer details:\n{new_customer}\nUsername: {new_user.username}'))
        click.echo(click.style("----------- CUSTOMER SUCCESSFULLY ADDED -----------", fg='green'))

    else:
        click.echo(click.style("Sorry! Customer already exists.", fg='red'))


@customer_management_group.command()
def update_customer():
    """-Update a customer record"""
    current_user = login()
    if current_user.role == 'employee':
        """-Update an existing customer record"""
        click.echo(click.style(f'{session.query(Customer).all()}', fg='yellow'))
        customer_id_to_update = click.prompt(
            click.style("Enter a number above to select the customer to update", fg='cyan'), type=int)
        customer_to_update = session.query(Customer).filter_by(id=customer_id_to_update).first()

        if customer_to_update:
            click.echo(f"{customer_to_update}")
            new_first_name = click.prompt(click.style("New first name", fg='cyan'))
            new_last_name = click.prompt(click.style("New last name", fg='cyan'))

            update_data = {
                Customer.first_name: new_first_name,
                Customer.last_name: new_last_name,
                Customer.full_name: f'{new_first_name} {new_last_name}'
            }

            session.query(Customer).filter_by(id=customer_to_update.id).update(update_data)
            session.commit()

            click.echo(
                click.style("------------ CUSTOMER NAME SUCCESSFULLY UPDATED -------------", fg='green', bold=True))
        else:
            click.echo(click.style("Selected customer does not exist and cannot be updated.", bold=True, fg='red'))
    else:
        click.echo(click.style("Sorry! You do not have permissions to access perform this action", fg='red'))


@customer_management_group.command()
def view_customer_details():
    """-View customer details"""
    current_user = login()
    if current_user.role == 'employee':
        """-View all details of a customer"""
        customer_view_choice = click.prompt(click.style(
            "Would you like to view all users or a specific user?\n1. All customers\n2.Specific customer\nSelect",
            fg='cyan'), type=int)
        if customer_view_choice == 1:
            customers = session.query(Customer).all()
            for customer in customers:
                click.echo(click.style(customer, fg='yellow'))
        if customer_view_choice == 2:
            customer_name = click.prompt(click.style("Enter name of customer", fg='cyan'))
            customer = session.query(Customer).filter(Customer.full_name.like(f"%{customer_name}%")).first()
            if customer:
                click.echo(click.style(customer, fg='yellow'))
            else:
                click.echo(click.style('Customer not found!', fg='yellow'))
    else:
        click.echo(click.style("Sorry! You do not have permissions to access perform this action", fg='red'))


@customer_management_group.command()
def delete_customer():
    """-Delete an existing customer record"""
    click.echo("Authorization required for delete action.")
    current_user = login()
    if current_user.role == 'employee':
        click.echo(click.style("Authorization Approved", fg='green'))
        click.echo(click.style(f'{session.query(Customer).all()}', fg='yellow'))
        customer_id_to_delete = click.prompt(
            click.style("Enter a number above to select the customer to delete", fg='cyan'), type=int)
        customer_to_delete = session.query(Customer).filter_by(id=customer_id_to_delete).first()
        print(customer_to_delete)

        if customer_to_delete:
            confirmation = click.prompt(click.style(
                "Please note that deleting a customer will cause related records in the 'purchases' table to be deleted as well. Continue? Y/N",
                fg='cyan'))
            if confirmation.lower() == 'y':
                session.delete(customer_to_delete)
                session.commit()
                user_to_delete = session.query(User).filter_by(customer_id=customer_to_delete.id).first()
                session.delete(user_to_delete)
                session.commit()
                click.echo(
                    click.style("------------------- CUSTOMER SUCCESSFULLY DELETED ---------------------", fg='green',
                                bold=True))
            if confirmation.lower() == 'n':
                click.echo("Delete Action Aborted!")
    else:
        click.echo(click.style("Sorry! You do not have permissions to access perform this action", fg='red'))


