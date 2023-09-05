from models import *
import click

if __name__ == '__main__':


    @click.group()
    def mycommands():
        pass


    categories = session.query(Category).all()
    suppliers = session.query(Supplier).all()
    products = session.query(Product).all()

    '''----------------------- C A T E G O R I E S ______________________--'''


    @mycommands.command()
    def view_categories():
        click.echo(session.query(Category).all())


    @mycommands.command()
    @click.option('--name', '-n', prompt="Enter the category name")
    def new_category(name):
        if name not in categories:
            new_category = Category(
                name=name
            )
            session.add(new_category)
            session.commit()
            click.echo(f"Category '{name}' successfully added!")
        else:
            click.echo(f"Category '{name}' already exists.")


    @mycommands.command()
    @click.option('--search_name', '-sn', prompt="Enter the category name to update")
    @click.option('--new_name', '-nn', prompt="Enter the name to be updated to")
    def update_category(search_name, new_name):
        category_to_update = session.query(Category).filter(Category.name.like(f'%{search_name}%')).first()
        click.echo(f"{category_to_update}")
        if category_to_update:
            session.query(Category).filter_by(id=category_to_update.id).update({
                Category.name: f'C-{new_name}'
            })
            session.commit()
            click.echo("Name successfully updated!")
        else:
            click.echo("Sorry! That category does not exist and cannot be updated.")


    @mycommands.command()
    @click.option('--search_name', '-sn', prompt="Enter the category name to delete")
    def delete_category(search_name):
        category_to_delete = session.query(Category).filter(Category.name.like(f'%{search_name}%')).first()
        click.echo(f"{category_to_delete}")
        if category_to_delete:
            session.delete(category_to_delete)
            session.commit()
            click.echo("Category successfully deleted!")
        else:
            click.echo("Sorry! That category does not exist and cannot be deleted.")


    @mycommands.command()
    @click.option('--category_name', '--cn', prompt="Enter the category to filter by")
    def view_category_products(category_name):
        click.echo(
            session.query(Product).join(Category.products).filter(Category.name.like(f'%{category_name}%')).all())

    '''----------------------- S U P P L I E R -------------------------'''
    @mycommands.command()
    def view_suppliers():
        click.echo(session.query(Supplier).all())


    @mycommands.command()
    @click.option('--name', '-n', prompt="Enter the supplier name")
    def new_supplier(name):
        if name.lower() not in [supplier.name.lower() for supplier in suppliers]:
            new_supplier = Supplier(
                name=name
            )
            session.add(new_supplier)
            session.commit()
            click.echo(f"Supplier '{name}' successfully added!")
        else:
            click.echo(f"Supplier '{name}' already exists.")


    @mycommands.command()
    @click.option('--search_name', '-sn', prompt="Enter the supplier name to update")
    @click.option('--new_name', '-nn', prompt="Enter the supplier name to update to")
    def update_supplier(search_name, new_name):
        supplier_to_update = session.query(Supplier).filter(Supplier.name.like(f'%{search_name}%')).first()
        click.echo(f"{supplier_to_update}")
        if supplier_to_update:
            session.query(Supplier).filter_by(id=supplier_to_update.id).update({
                Supplier.name: f'C-{new_name}'
            })
            session.commit()
            click.echo("Supplier name successfully updated!")
        else:
            click.echo("Sorry! That supplier does not exist and cannot be updated.")


    @mycommands.command()
    @click.option('--search_name', '-sn', prompt="Enter the category name to delete")
    def delete_supplier(search_name):
        supplier_to_delete = session.query(Supplier).filter(Supplier.name.like(f'%{search_name}%')).first()
        click.echo(f"{supplier_to_delete}")
        if supplier_to_delete:
            session.delete(supplier_to_delete)
            session.commit()
            click.echo("Supplier successfully deleted!")
        else:
            click.echo("Sorry! That supplier does not exist and cannot be deleted.")

    @mycommands.command()
    @click.option('--search_supplier', '-ssup', prompt="Enter name of the supplier to see related products")
    def view_supplier_products(search_supplier):
        click.echo(session.query(Product).join(Product.supplier).filter(Supplier.name.like(f'%{search_supplier}%')).all())


    '''----------------------- P R O D U C T S -------------------------'''

    @mycommands.command()
    def view_products():
        products = session.query(Product)
        for product in products:
            click.echo(f'({product.id}): Name:{product.name}, Price:{product.price} | Quantity:{product.quantity} | Category:{product.category.name} | Product:{product.supplier.name}')















    # Invoke mycommands method which calls all the commands
    mycommands()
