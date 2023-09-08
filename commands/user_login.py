import click
from models.models import *

global current_user



def login():
    username = click.prompt(click.style("Enter your username", fg='cyan'))
    password = click.prompt(click.style("Enter password", fg='cyan'),hide_input=True)
    user_record = session.query(User).filter(User.username.like(f'%{username}%')).first()
    if user_record and user_record.password == password:
        current_user = user_record
        click.echo(click.style(f'Logged in successfully as {user_record.username}'))
        # click.echo(click.style(f'------- LOGIN SUCCESSFUL --------', fg='green'))
        return current_user
    else:
        click.echo(click.style('Login failed. Please check your credentials.', fg='red'))
        return

