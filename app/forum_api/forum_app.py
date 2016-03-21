from app import app
from flask import jsonify, request, Blueprint
from DBConfig import *
from app import db_tools, functions
import forum_tools
import urlparse
import json

app = Blueprint('forum_app', __name__)


@app.route('/create/', methods=['POST'])
def create_forum():
    connection = db_tools.connect()
    params = request.json

    try:

        functions.check(params, ["name", "short_name", "user"])
        response = forum_tools.create(connection, params["name"], params[
                                "short_name"], params["user"])

    except Exception as e:
        connection.close()
        return json.dumps({"code": 3, "response": (e.message)})

    connection.close()
    return json.dumps({"code": 0, "response": response})


@app.route('/details/', methods=['GET'])
def details():
    connection = db_tools.connect()
    params = functions.get_json(request)

    try:
        functions.check(params, ["forum"])
        response = forum_tools.details(
            connection, params["forum"], functions.get_related(params))

    except Exception, e:
        return json.dumps({"code": 3, "response": (e.message)})

    connection.close()

    return json.dumps({"code": 0, "response": response})


@app.route('/listPosts/', methods=['GET'])
def list_posts():
    connection = db_tools.connect()
    params = functions.get_json(request)
    optional = functions.get_optional(
        params,
        ["since",
         "limit",
         "order"]
    )
    related = functions.get_related(params)
    try:
        functions.check(params, ["forum"])
        response = post_tools.posts_list(connection, entity="forum", params=optional, identifier=params[
                                   "forum"], related=related)
    except Exception, e:
        return json.dumps({"code": 3, "response": (e.message)})
    connection.close()
    return json.dumps({"code": 0, "response": response})


@app.route('/listThreads/', methods=['GET'])
def list_threads():
    connection = db_tools.connect()
    params = functions.get_json(request)
    optional = functions.get_optional(params, ["since", "limit", "order"])
    related = functions.get_related(params)
    try:
        functions.check(params, ["forum"])
        response = thread_tools.list(connection=connection, optional=optional,
                               required=params, related=related)
    except Exception, e:
        return json.dumps({"code": 3, "response": (e.message)})
    connection.close()
    return json.dumps({"code": 0, "response": response})


@app.route('/listUsers/', methods=['GET'])
def list_users():
    connection = db_tools.connect()
    params = functions.get_json(request)
    optional = functions.get_optional(params, ["since_id", "limit", "order"])
    try:
        functions.check(params, ["forum"])
        response = forum_tools.list_users(
            connection=connection, optional=optional, forum_shortname=params["forum"][0])
    except Exception, e:
        connection.close
        return json.dumps({"code": 3, "response": (e.message)})
    connection.close()
    return json.dumps({"code": 0, "response": response})