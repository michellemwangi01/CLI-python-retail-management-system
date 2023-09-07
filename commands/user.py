import click
from models.models import *

global current_user


def login():
    username = click.prompt("Enter your username")
    password = click.prompt("Enter password", hide_input=True)
    user_record = session.query(User).filter(User.username.like(f'%{username}%')).first()
    if user_record and user_record.password == password:
        current_user = user_record
        click.echo(click.style(f'Logged in as {user_record.username}'))
        click.echo(click.style(f'------- LOGIN SUCCESSFUL --------', fg='green'))
    else:
        click.echo('Login failed. Please check your credentials.')
    return current_user



