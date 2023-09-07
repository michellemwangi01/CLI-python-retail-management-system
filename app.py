import click
from commands.sales import sales_management_group
from commands.inventory import inventory_management_group
from commands.supplier import supplier_management_group
from commands.product import product_management_group
from commands.customer import customer_management_group
from commands.user_login import *


@click.group()
def mycommands():
    '''Collect the command groups into one group'''
    pass



if __name__ == '__main__':
    # _------------------------------ Add Command Groups to main group ------------------------

    mycommands.add_command(inventory_management_group)
    mycommands.add_command(supplier_management_group)
    mycommands.add_command(customer_management_group)
    mycommands.add_command(product_management_group)
    mycommands.add_command(sales_management_group)
    mycommands()

# Loyalty points for customers
# User Authentication (profiles) - clients(make purchase, view purchase history, view popular products and categories)
# - Admin (add stuff, place orders, manage suppliers, categories, products
# allow a new customer to be created as they are making a purchase
