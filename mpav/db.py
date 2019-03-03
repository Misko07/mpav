from flask.cli import with_appcontext
from flask import current_app, g
import sqlite3
import click
import json
import os


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

    # todo test this
    populate_db()


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


def populate_db():

    projects_json = "mpav/projects/projects.json"
    if os.path.isfile(projects_json):
        with open(projects_json, "r") as file:
            project_list = json.load(file)
    else:
        raise FileNotFoundError("Missing projects.json file.")

    # Get short and long description files
    files = os.listdir("mpav/projects/")
    mds_short = [file for file in files if file[-9:] == "-short.md"]
    mds_long = [file for file in files if file[-8:] == "-long.md"]
    print(mds_short)
    print(mds_long)

    # Add descriptions to projects
    for project in project_list:
        project['sdesc'] = ""
        project['ldesc'] = ""

        for md_short in mds_short:
            if project['title'] in md_short:
                with open("mpav/projects/%s" % md_short) as file:
                    project['sdesc'] = file.read()

        for md_long in mds_long:
            if project['title'] in md_long:
                with open("mpav/projects/%s" % md_long) as file:
                    project['ldesc'] = file.read()

    # Insert projects in db
    db = get_db()
    cur = db.cursor()
    for project in project_list:
        print(project)

        project['tools'] = ",".join([tool for tool in project['tools']])

        vals = [
            project['title'],
            project['category'],
            project['sdesc'],
            project['ldesc'],
            project['tools'],
            project['period']
        ]

        cur.execute(
            'INSERT INTO projects (title, category, sdesc, ldesc, tools, period)'
            ' VALUES (?, ?, ?, ?, ?, ?)', vals)
        db.commit()

        print(cur.rowcount, "record inserted.")

        prs = db.execute('SELECT * FROM projects').fetchall()
        print(prs[0]['title'])

