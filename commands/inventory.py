import click
from models.models import *

@click.group(name='inventory', help='--Inventory management commands')
def inventory_management_group():
    pass

@inventory_management_group.command()
def view_categories():
    '''View list of all categories'''
    click.echo(session.query(Category).all())


@inventory_management_group.command()
@click.option('--name', '-n', prompt="Enter the category name")
def new_category(name):
    '''Add a new category'''
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


@inventory_management_group.command()
@click.option('--search_name', '-sn', prompt="Enter the category name to update")
@click.option('--new_name', '-nn', prompt="Enter the name to be updated to")
def update_category(search_name, new_name):
    '''Update existing category details'''
    category_to_update = session.query(Category).filter(Category.name.like(f'%{search_name}%')).first()
    click.echo(f"{category_to_update}")
    if category_to_update:
        session.query(Category).filter_by(id=category_to_update.id).update({
            Category.name: f'C-{new_name}'
        })
        session.commit()
        click.echo(click.style("-------------- NAME SUCCESSFULLY UPDATED -------------", fg='green', bold=True))
    else:
        click.echo(
            click.style(" *** Sorry! That category does not exist and cannot be updated. ***", fg='red', bold=True))


@inventory_management_group.command()
@click.option('--search_name', '-sn', prompt="Enter the category name to delete")
def delete_category(search_name):
    '''delete a category'''
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
                    click.echo(click.style("No related products found!", fg='red', bold=True))
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
