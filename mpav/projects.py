from mpav.db import get_db

from flask import (
    g, render_template, request, session, url_for, Blueprint
)

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
