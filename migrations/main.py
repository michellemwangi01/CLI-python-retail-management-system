import click
from models import *

categories = session.query(Category.name.toLower()).all()

@click.group()
def mycommands():
    pass


@mycommands.command()
@click.option('--name', '-n', prompt="Enter the category name")
def new_category(name):
    if name not in categories:
        session.add(name)
        session.commit()
    else:
        click.echo(f"Category '{name}' already exists.")