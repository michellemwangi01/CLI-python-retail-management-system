purchase_details = ("customer", "product", "quantity")
@mycommands.command()
@click.option('--choice', '-n', prompt="What column would you like to update? Select",
              type=click.Choice(purchase_details))
@click.option('--customer_name', '-cn', prompt="Which purchase record would you like to update? (customer name)")
@click.option('--product_name', '-pn', prompt="Which purchase record would you like to update? (product name)")
def update_purchase(choice, customer_name, product_name ):
    purchase_to_update = session.query(Purchase).filter(and_(
        Purchase.customer.name.like(f'%{customer_name}%'),
        Purchase.product.name.like(f'%{product_name}%')
    )).first()
    print(purchase_to_update)
    update_data = {}
    if purchase_to_update:
        click.echo(f"{purchase_to_update}")
        if choice.lower() == 'quantity':
            new_quantity = click.prompt("Enter the new quantity")
            update_data['quantity'] = new_quantity

        # update foreign key values
        if choice.lower() == 'customer':
            update_to_customer = click.prompt("Enter the new customer name")
            customer_record = session.query(Supplier).filter(Supplier.name.like(f'%{update_to_customer}%')).first()
            if customer_record:
                update_data['customer_id'] = customer_record.id
            else:
                click.echo(
                    "Entered customer does not exist. View existing purchases using the 'view-purchases' command.")
        if choice.lower() == 'product':
            update_to_product = click.prompt("Enter the new product name")
            product_record = session.query(Category).filter(Category.name.like(f'%{update_to_product}%')).first()
            if product_record:
                update_data['product_id'] = product_record.id
            else:
                click.echo(
                    "Entered product does not exist. View existing products using the 'view-products' command.")
        print(update_data)
        session.query(Product).filter_by(id=purchase_to_update.id).update(update_data)
        session.commit()
        click.echo("Purchase is successfully updated!")
    else:
        click.echo(
            "Sorry! That purchase record does not exist and cannot be updated. View existing purchases using the 'view-purchase-details' command.")


table_options = {
    "products": Product,
    "categories": Category,
    "suppliers": Supplier,
    "customers": Customer,
    "purchases": Purchase
}
@mycommands.command()
@click.option('--choice', '-n', prompt="Table to delete from? Select", type=click.Choice(table_options))
@click.option('--name', '-n', prompt="Record from the table to delete (name)")

def delete_records(choice, name):
    print(choice, name)
    record_to_delete = session.query(table_options[choice]).filter(table_options[choice].name.like(f'%{name}%')).first()
    print(record_to_delete)
    if record_to_delete:
        session.delete(record_to_delete)
        session.commit()
        click.echo("Product has been successfully deleted")
    else:
        click.echo("Error! No such product exists.")
