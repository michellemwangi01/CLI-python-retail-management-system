from models import *
import click

if __name__ == '__main__':

    categories = session.query(Category.name).all()


    @click.group()
    def mycommands():
        pass

        '''----------------------- C A T E G O R I E S ______________________--'''
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
            session.query(Category).filter_by(id = category_to_update.id).update({
                Category.name: f'C-{new_name}'
            })
            session.commit()
            click.echo("Name successfully updated!")
        else:
            click.echo("Sorry! That category does not exist and cannot be updated.")



if __name__ == '__main__':
    mycommands()
