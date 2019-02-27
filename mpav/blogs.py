from mpav.db import get_db

from flask import (
    g, render_template, request, session, url_for, Blueprint
)
from werkzeug.exceptions import abort

bp = Blueprint('blogs', __name__)


@bp.route('/')
def get_blogs():

    db = get_db()

    posts = db.execute(
        "SELECT * FROM blogs"
    ).fetchall()

    print('len(blogs):', len(posts))

    return render_template("index.html", posts=posts)
