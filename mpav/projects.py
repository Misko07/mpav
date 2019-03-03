from mpav.db import get_db
import os

from flask import (
    g, render_template, request, session, url_for, Blueprint, Markup
)
import markdown
from werkzeug.exceptions import abort

bp = Blueprint('projects', __name__)


@bp.route('/projects', methods=('GET', 'POST'))
def get_projects():
    db = get_db()

    projects = db.execute(
        'SELECT * FROM projects'
    ).fetchall()

    projects2 = []
    for project in projects:
        project2 = dict(project)
        project2['tools'] = list(project2['tools'].split(","))
        projects2.append(dict(project2))

    return render_template('projects.html', projects=projects2)


def get_project(id_):

    project = get_db().execute(
        'SELECT id, title, ldesc from projects where id = ?', (id_,)
    ).fetchone()

    if project is None:
        abort(404, "Project id {0} does not exist".format(id_))

    # Convert project's description from markdown to html
    project2 = dict(project)
    project2['ldesc'] = Markup(markdown.markdown(project2['ldesc']))

    return project2


@bp.route('/projects/project-<int:id>', methods=('GET', 'POST'))
def show(id):
    project = get_project(id)

    return render_template('project.html', project=project)


def _get_markup(project_name):

    filepath = "mpav/projects/%s-short.md" % project_name

    if os.path.isfile(filepath):
        with open(filepath, "r") as file:
            short_desc = Markup(markdown.markdown(file.read()))
        print(short_desc)
        return short_desc
    return None
