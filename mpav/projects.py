from mpav.db import get_db

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
        'SELECT id, title, sdesc'
        ' FROM projects'
    ).fetchall()
    return render_template('projects.html', projects=projects)


def get_project(id_):

    project = get_db().execute(
        'SELECT id, title, ldesc from projects where id = ?', (id_,)
    ).fetchone()

    if project is None:
        abort(404, "Project id {0} does not exist".format(id_))

    # Convert project's description from markdown to html
    project2 = {}
    for key in project.keys():
        project2[key] = project[key]
    project2['ldesc'] = Markup(markdown.markdown(project2['ldesc']))

    return project2


@bp.route('/project/project-<int:id>', methods=('GET', 'POST'))
def show(id):
    project = get_project(id)

    return render_template('project.html', project=project)


