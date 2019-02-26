from mpav.db import get_db

from flask import (
    g, render_template, request, session, url_for, Blueprint
)
from werkzeug.exceptions import abort

bp = Blueprint('projects', __name__)


@bp.route('/projects', methods=('GET', 'POST'))
def get_projects():
    db = get_db()

    projects = db.execute(
        'SELECT id, title, sdesc'
        ' FROM project'
    ).fetchall()
    print('num projects:', len(projects))
    return render_template('projects.html', projects=projects)


def get_project(id_):

    project = get_db().execute(
        'SELECT id, title, ldesc from project where id = ?', (id_,)
    ).fetchone()

    if project is None:
        abort(404, "Project id {0} does not exist".format(id_))

    return project


@bp.route('/project/<int:id>', methods=('GET', 'POST'))
def show(id):
    project = get_project(id)

    return render_template('project_template.html', project=project)


