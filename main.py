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
        click.echo(
            session.query(Product).join(Product.supplier).filter(Supplier.name.like(f'%{search_supplier}%')).all())


    '''----------------------- P R O D U C T S -------------------------'''


    @mycommands.command()
    @click.option('--name', '-pn', default=None, type=str, help="Search for a product by name")
    def view_product_details(name):
        if name is None:
            for product in session.query(Product):
                click.echo(
                    f'({product.id}): Name:{product.name}, Price:{product.price} | Quantity:{product.quantity} | Category:{product.category.name} | Product:{product.supplier.name}')
        else:
            product = session.query(Product).filter(Product.name.like(f'%{name}%')).first()
            if product:
                click.echo(
                    f'({product.id}): Name:{product.name}, Price:{product.price} | Quantity:{product.quantity} | Category:{product.category.name} | Product:{product.supplier.name}')
            else:
                click.echo("Product you searched fo does not exist.")


    @mycommands.command()
    @click.option('--name', '-n', prompt="Enter the product name", type=str)
    @click.option('--category', '-c', prompt="Enter the category", type=str)
    @click.option('--supplier', '-s', prompt="Enter the supplier name", type=str)
    @click.option('--price', '-p', prompt="Enter the price", type=float)
    @click.option('--quantity', '-q', prompt="Enter the quantity", type=int)
    def add_product(name, category, supplier, price, quantity):
        category_record = session.query(Category).filter(Category.name.like(f'%{category}%')).first()
        supplier_record = session.query(Supplier).filter(Supplier.name.like(f'%{supplier}%')).first()
        click.echo(category_record)
        click.echo(supplier_record)
        if category_record and supplier_record:
            new_product = Product(
                name=f'P-{name}',
                supplier_id=supplier_record.id,
                category_id=category_record.id,
                price=price,
                quantity=quantity,
            )
            session.add(new_product)
            session.commit()
            click.echo("New product added successfully!")
        else:
            click.echo("Sorry! Category or Supplier you entered does not exist.")


    @mycommands.command()
    @click.option('--name', '-n', help="Search for product to delete", prompt="Enter product name to be deleted")
    def delete_product(name):
        product_to_delete = session.query(Product).filter(Product.name.like(f'%{name}%')).first()
        if product_to_delete:
            session.delete(product_to_delete)
            session.commit()
            click.echo("Product has been successfully deleted")
        else:
            click.echo("Error! No such product exists.")


    # @mycommands.command()
    # @click.option('--name', '-n', prompt="Enter the product to update")
    # @click.option('--new_name', '-n', default=None)
    # @click.option('--price', '-p', type=int, default=None)
    # @click.option('--supplier', '-s', default=None)
    # @click.option('--category', '-c', default=None)
    # @click.option('--quantity', '-c', type=int, default=None)
    # def update_products(name, new_name, price, quantity, supplier, category):
    #     update_data = {}
    #     product_to_update = session.query(Product).filter(Product.name.like(f'%{name}%')).first()
    #     print(product_to_update.id)
    #     if product_to_update:
    #         click.echo(f"{product_to_update}")
    #         if new_name is not None:
    #             update_data['name'] = f'P-{new_name}'
    #         if price is not None:
    #             update_data['price'] = price
    #         if quantity is not None:
    #             update_data['quantity'] = quantity
    #
    #         if supplier:
    #             supplier_record = session.query(Supplier).filter(Supplier.name.like(f'%{supplier}%')).first()
    #             if supplier_record:
    #                 update_data['supplier_id'] = supplier_record.id
    #             else:
    #                 click.echo("Entered supplier does not exist")
    #         if category:
    #             category_record = session.query(Category).filter(Category.name.like(f'%{category}%')).first()
    #             if category_record:
    #                 update_data['category_id'] = category_record.id
    #             else:
    #                 click.echo("Entered category does not exist")
    #
    #         session.query(Product).filter_by(id=product_to_update.id).update(update_data)
    #         session.commit()
    #         click.echo("Product is successfully updated!")
    #     else:
    #         click.echo("Sorry! That product does not exist and cannot be updated.")

    @mycommands.command()
    @click.option('--name', '-n', prompt="Enter the product to update")
    @click.option('--new_name', '-nn', default=None)
    @click.option('--price', '-p', type=int, default=None)
    @click.option('--supplier', '-s', default=None)
    @click.option('--category', '-c', default=None)
    @click.option('--quantity', '-q', type=int, default=None)
    def update_products(name, new_name, price, quantity, supplier, category):
        update_data = {}
        product_to_update = session.query(Product).filter(Product.name.like(f'%{name}%')).first()

        if product_to_update:
            click.echo(f"{product_to_update}")

            if new_name is not None:
                update_data['name'] = f'P-{new_name}'
            if price is not None:
                update_data['price'] = price
            if quantity is not None:
                update_data['quantity'] = quantity

            if supplier:
                supplier_record = session.query(Supplier).filter(Supplier.name.like(f'%{supplier}%')).first()
                if supplier_record:
                    update_data['supplier_id'] = supplier_record.id
                else:
                    click.echo("Entered supplier does not exist")

            if category:
                category_record = session.query(Category).filter(Category.name.like(f'%{category}%')).first()
                if category_record:
                    update_data['category_id'] = category_record.id
                else:
                    click.echo("Entered category does not exist")
            print(update_data)
            session.query(Product).filter_by(id=product_to_update.id).update(update_data)
            session.commit()
            click.echo("Product is successfully updated!")
        else:
            click.echo("Sorry! That product does not exist and cannot be updated.")


    # Invoke mycommands method which calls all the commands
    mycommands()
