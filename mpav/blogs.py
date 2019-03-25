from .db import get_db

from flask import (
    g, render_template, request, session, url_for, Blueprint
)
from werkzeug.exceptions import abort

bp = Blueprint('blogs', __name__)


@bp.route('/')
def get_blogs():

    posts = []

    return render_template("index.html", posts=posts)
