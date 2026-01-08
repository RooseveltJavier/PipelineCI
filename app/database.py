import click

from flask import current_app

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(current_app.config['DB_CONNECTION'], echo=True)
db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine))

DBModel = declarative_base()
DBModel.query = db_session.query_property()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)    
    app.cli.add_command(create_user_command)


def close_db(e=None):
    db_session.remove()


@click.command('init-db')
def init_db_command():
    from app import models

    DBModel.metadata.create_all(bind=engine)


@click.command('create-user')
@click.argument('login')
def create_user_command(login):
    from app.models import User
    from werkzeug.security import generate_password_hash

    password = click.prompt('Password')

    user = User()
    user.login = login
    user.password = generate_password_hash(password)

    db_session.add(user)
    db_session.commit()