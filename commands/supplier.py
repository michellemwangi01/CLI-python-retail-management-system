import click
from models.models import *

'''----------------------- S U P P L I E R -------------------------'''
@click.group(name='supplier', help='--Supplier management commands')
def supplier_management_group():
    pass

@supplier_management_group.command()
def view_suppliers():
    '''View list of all suppliers'''
    suppliers = session.query(Supplier).all()
    for supplier in suppliers:
        click.echo(click.style(f"{supplier}", fg='yellow'))

@supplier_management_group.command()
@click.option('--name', '-n', prompt="Enter the supplier name")
def new_supplier(name):
    '''Add a new supplier'''
    suppliers = session.query(Supplier)
    if name.lower() not in [supplier.name.lower() for supplier in suppliers]:
        new_supplier = Supplier(
            name=name
        )
        session.add(new_supplier)
        session.commit()
        click.echo(click.style(f"---------------- SUPPLIER SUCCESSFULLY ADDED ---------------", fg='green', bold=True))
    else:
        click.echo(click.style(f"Supplier '{name}' already exists.", fg="red"))


@supplier_management_group.command()
def update_supplier():
    """update an existing supplier record"""
    click.echo(click.style(f'{session.query(Supplier).all()}', fg='yellow'))
    supplier_id_to_update = click.prompt(
        click.style("Choose a number above to select the supplier to update", fg='cyan'), type=int)
    supplier_to_update = session.query(Supplier).filter_by(id=supplier_id_to_update).first()
    click.echo(supplier_to_update)
    new_supplier_name = click.prompt(click.style("New supplier name", fg='cyan'))

    if supplier_to_update:
        session.query(Supplier).filter_by(id=supplier_to_update.id).update({
            Supplier.name: f'C-{new_supplier_name}'
        })
        session.commit()
        click.echo(click.style("Supplier name successfully updated!", fg='green', bold=True))
    else:
        click.echo(click.style("ERROR! That supplier does not exist and cannot be updated.", bold=True, fg='red'))


@supplier_management_group.command('')
def delete_supplier():
    '''Delete an existing supplier'''
    click.echo(click.style(f'{session.query(Supplier).all()}', fg='yellow'))
    supplier_id_to_delete = click.prompt(
        click.style("Choose a number above to select the supplier to delete", fg='cyan'), type=int)
    supplier_to_delete = session.query(Supplier).filter_by(id=supplier_id_to_delete).first()
    click.echo(supplier_to_delete)
    if supplier_to_delete:
        confirmation = click.prompt(click.style(
            "To complete delete, related product records will be updated to a different supplier via auto-assign or selected supplier. Continue? Y/N",
            fg='cyan'))
        if confirmation.lower() == 'y':
            supplier_update_mode = click.prompt(click.style(
                "Update via auto-assign or selected supplier? Enter 1 or 2 to choose.\n1. Auto-assign (1)\n2. Select Supplier(2)\nEnter Selection",
                fg='cyan'), type=int)
            if supplier_update_mode == 1:
                products_to_update_supplier = session.query(Product).filter(
                    Product.supplier_id == supplier_to_delete.id).all()
                if products_to_update_supplier:
                    suppliers = session.query(Supplier).filter(Supplier.id != supplier_to_delete.id).all()
                    random_supplier = random.choice(suppliers)
                    session.query(Product).filter(Product.supplier_id == supplier_to_delete.id).update(
                        {
                            Product.supplier_id: random_supplier.id
                        }
                    )
                    click.echo(click.style(f"Product Suppliers successfully updated to {random_supplier}!", fg='green',
                                           bold=True))
                    session.delete(supplier_to_delete)
                    session.commit()
                    click.echo(click.style("------------------- SUPPLIER SUCCESSFULLY DELETED ---------------------",
                                           fg='green', bold=True))
                else:
                    click.echo(click.style("No related products found!", fg='red'))
            elif supplier_update_mode == 2:
                new_supplier_name = click.prompt(
                    click.style("Which supplier would you like to transfer the product records to?", fg='cyan'))
                new_supplier = session.query(Supplier).filter(Supplier.name.like(f'%{new_supplier_name}%')).first()
                session.query(Product).filter(Product.supplier_id == supplier_to_delete.id).update(
                    {
                        Product.supplier_id: new_supplier.id
                    }
                )
                click.echo(
                    click.style(f"Product Suppliers successfully updated to {new_supplier}!", fg='green', bold=True))
                session.delete(supplier_to_delete)
                session.commit()
                click.echo(
                    click.style("------------------- SUPPLIER SUCCESSFULLY DELETED ---------------------", fg='green',
                                bold=True))
            else:
                click.command(click.style("ERROR! Input Invalid", fg='red', bold=True))
        elif confirmation.lower() == 'n':
            click.echo(click.style("--------------- Delete Action Aborted ----------------", fg='red', bold=True))
        else:
            click.echo(click.style("ERROR! Invalid input!", fg='red', bold=True))
    else:
        click.echo(click.style("Sorry! That supplier does not exist and cannot be deleted.", fg='red', bold=True))

