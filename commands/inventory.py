import click
from models.models import *
from commands.user import login



# current_user = login()
#     if current_user.role == 'Employee':
#
#     else:
#         click.echo(click.style("Sorry! You do not have permissions to access perform this action", fg='red'))
@click.group(name='inventory', help='--Inventory management commands')
def inventory_management_group():
    pass

@inventory_management_group.command()
def view_categories():
    """-View list of all categories"""
    click.echo(session.query(Category).all())


@inventory_management_group.command()
@click.option('--name', '-n', prompt="Enter the category name")
def new_category(name):
    """-Add a new category"""
    categories = session.query(Category)
    if name not in categories:
        new_category = Category(
            name=name
        )
        session.add(new_category)
        session.commit()
        click.echo(f"Category Added: {new_category}")
        click.echo(click.style(f"--------------- CATEGORY SUCCESSFULLY ADDED ----------------", fg='green', bold=True))
    else:
        click.echo(click.style(f"*** Category '{name}' already exists. ***", fg='red'))


@inventory_management_group.command()
def update_category():
    """-Update existing category details"""
    current_user = login()
    if current_user.role == 'Employee':
        click.echo(click.style(session.query(Category).all(), fg='yellow'))
        category_id = click.prompt(click.style("Select the category number to update", fg='cyan'))
        category_to_update = session.query(Category).filter_by(id=category_id).first()
        click.echo(f"{category_to_update}")
        new_category_name = click.prompt(click.style("Enter new product name", fg='cyan'))
        if category_to_update:
            session.query(Category).filter_by(id=category_to_update.id).update({
                Category.name: new_category_name
            })
            session.commit()
            click.echo(click.style("-------------- NAME SUCCESSFULLY UPDATED -------------", fg='green', bold=True))
        else:
            click.echo(
                click.style(" *** Sorry! That category does not exist and cannot be updated. ***", fg='red', bold=True))

    else:
        click.echo(click.style("Sorry! You do not have permissions to access perform this action", fg='red'))



@inventory_management_group.command()
# @click.option('--search_name', '-sn', prompt="Enter the category name to delete")
def delete_category():
    """-Delete a category"""
    current_user = login()
    if current_user.role == 'Employee':
        click.echo(click.style("Authorization Approved!",fg='green'))
        click.echo(click.style(f'{session.query(Category).all()}', fg='yellow'))
        category_id_to_update = click.prompt(
            click.style("Enter a number above to select the category to update", fg='cyan'), type=int)
        category_to_delete = session.query(Customer).filter_by(id=category_id_to_update).first()
        if category_to_delete:
            confirmation = click.prompt(
               click.style("To complete delete, related product records will be updated to a different supplier via auto-assign or selected supplier. Continue? Y/N", fg='cyan'))
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
                        click.echo(
                            click.style(f"Product categories successfully updated to {random_category}", fg='green',
                                        bold=True))
                        session.delete(category_to_delete)
                        session.commit()
                        click.echo(
                            click.style("------------------- CATEGORY SUCCESSFULLY DELETED ---------------------",
                                        fg='green', bold=True))
                    else:
                        click.echo(click.style("No category or related products found!", fg='red'))
                elif category_update_mode == 2:
                    new_category_name = click.prompt(
                        click.style("Which category would you like to transfer the product records to?", fg='cyan',
                                    bold=True))
                    new_category = session.query(Category).filter(Category.name.like(f'%{new_category_name}%')).first()
                    session.query(Product).filter(Product.supplier_id == category_to_delete.id).update(
                        {
                            Product.category_id: new_category.id
                        }
                    )
                    click.echo(
                        click.style(f"Product categories successfully updated to {new_category}!", fg='green',
                                    bold=True))
                    session.delete(category_to_delete)
                    session.commit()
                    click.echo(
                        click.style("------------------- CATEGORY SUCCESSFULLY DELETED ---------------------",
                                    fg='green',
                                    bold=True))
                else:
                    click.echo(click.style("ERROR! Input Invalid", fg='red', bold=True))
            elif confirmation.lower() == 'n':
                click.echo(click.style("Delete Action Aborted!", fg='red', bold=True))
            else:
                click.echo(click.style("ERROR! Invalid input!", fg='red', bold=True))
        else:
            click.echo(click.style("ERROR! That category does not exist and cannot be deleted.", fg='red', bold=True))
    else:
        click.echo(click.style("Sorry! You do not have permissions to access perform this action", fg='red'))
