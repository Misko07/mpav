import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """
    Reuse the same DB connection if already active in a given request
    :return: A db connection
    """

    # - g - a namespace object that can store data during an application context (request)
    # - current_app - a special object that points to the Flask app, for handling the request
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Return rows that behave like dicts. This allows accessing the columns by name
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    Close  the connection if exists in `g`
    :param e:
    :return: /
    """

    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
    Create the table schema if not existing
    :return: /
    """

    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    with current_app.open_resource('schema_init.sql') as f:
        db.executescript(f.read().decode('utf8'))


# Define a command line command `init-db`
@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    Initialise db - clear the existing data and create new tables
    :return: /
    """
    init_db()
    click.echo("Initialised the database.")


def init_app(app):
    """
    Register `init_db` and `close_db` with an app. This function will be imported and executed in the factory.

    :param app: A Flask app instance
    :return: /
    """

    # What function to call when cleaning up after returning the response
    app.teardown_appcontext(close_db)

    # Add a new command that can be called with the flask command
    app.cli.add_command(init_db_command)

