import json
import os

from flask import (
    g, render_template, request, session, url_for, Blueprint, Markup
)
import markdown
from werkzeug.exceptions import abort

bp = Blueprint('projects', __name__)


def project_generator():
    print('*** in show')
    projects_json = "mpav/projects/projects.json"
    if os.path.isfile(projects_json):
        with open(projects_json, "r") as file:
            project_list = json.load(file)
    print('***pl', project_list)
    for p in project_list:
        print('**title:', p['title'])
        yield {'title': p['title']}


def get_projects_list():
    projects_json = "mpav/projects/projects.json"
    if os.path.isfile(projects_json):
        with open(projects_json, "r") as file:
            project_list = json.load(file)
    return project_list


def get_project_descriptions(title):

    # Get short and long description files
    files = os.listdir("mpav/projects/")
    mds_short = [file for file in files if file[-9:] == "-short.md"]
    mds_long = [file for file in files if file[-8:] == "-long.md"]
    print(mds_short)
    print(mds_long)

    short = None
    long = None

    for filename in mds_short:
        if title in filename:
            with open("mpav/projects/%s" % filename) as file:
                short = file.read()

    for filename in mds_long:
        if title in filename:
            with open("mpav/projects/%s" % filename) as file:
                long = file.read()

    return long, short


@bp.route('/projects', methods=('GET', 'POST'))
def get_projects():

    project_list = get_projects_list()

    # projects2 = []
    # for project in projects:
    #     project2 = dict(project)
    #     project2['tools'] = list(project2['tools'].split(","))
    #     projects2.append(dict(project2))

    return render_template('projects.html', projects=project_list)


def get_project(title):

    print('title', title)

    project = None
    projects_json = "mpav/projects/projects.json"
    if os.path.isfile(projects_json):
        with open(projects_json, "r") as file:
            project_list = json.load(file)
    else:
        raise FileNotFoundError("Missing projects.json file.")

    for pj in project_list:
        if pj['title'] == title:
            project = dict(pj)

    # if project is None:
    #     abort(404, "Project {0} does not exist".format(title))

    # Get long / short descriptions of project
    project['ldesc'], project['sdesc'] = get_project_descriptions(title)

    # Convert project's description from markdown to html
    project['ldesc'] = Markup(markdown.markdown(project['ldesc']))

    return project


@bp.route('/projects/<string:title>', methods=('GET', 'POST'))
def show(title):
    project = get_project(title)

    return render_template('project.html', project=project)


def _get_markup(project_name):

    filepath = "mpav/projects/%s-short.md" % project_name

    if os.path.isfile(filepath):
        with open(filepath, "r") as file:
            short_desc = Markup(markdown.markdown(file.read()))
        print(short_desc)
        return short_desc
    return None
