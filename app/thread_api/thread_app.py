from app import app
from flask import jsonify, request, Blueprint
from DBConfig import *
from app import db_tools, functions
from app.post_api import post_tools
import thread_tools
import json

app = Blueprint('thread_app', __name__)


@app.route('/create/', methods=['GET', 'POST'])
def create_thread():

    connection = db_tools.connect()
    params = request.json

    optional = functions.get_optional(params, ["isDeleted"])

    try:
        functions.check(
            params, ["forum", "title", "isClosed", "user", "date", "message", "slug"])

        response = thread_tools.create(connection, params["forum"], params["title"], params["isClosed"], params[
                                 "user"], params["date"], params["message"], params["slug"], optional)

    except Exception as e:
        connection.close()
        return json.dumps({"code": 3, "response": (e.message)})

    connection.close()
    return json.dumps({"code": 0, "response": response})


@app.route("/details/", methods=["GET"])
def details_thread():

    connection = db_tools.connect()
    params = functions.get_json(request)
    required_data = ["thread"]
    related = functions.get_related(params)

    if 'thread' in related:
        connection.close()
        return json.dumps({"code": 3, "response": "error"})
    try:
        functions.check(params, required_data)
        response = thread_tools.details(connection, params["thread"], related)
    except Exception as e:
        connection.close()
        return json.dumps({"code": 1, "response": (e.message)})
    connection.close()
    return json.dumps({"code": 0, "response": response})


@app.route("/vote/", methods=['POST'])
def vote_thread():

    connection = db_tools.connect()
    params = request.json

    try:
        functions.check(params, ["vote", "thread"])
        response = thread_tools.vote(connection=connection, vote=params[
                               "vote"], thread=params["thread"])
    except Exception as e:
        connection.close()
        return json.dumps({"code": 1, "response": (e.message)})
    connection.close()
    return json.dumps({"code": 1, "response": response})


@app.route("/update/", methods=['POST'])
def update_thread():

    connection = db_tools.connect()

    params = request.json

    try:
        functions.check(params, ["message", "slug", "thread"])
        response = thread_tools.update(connection=connection, message=params["message"], slug=params[
                                 "slug"], thread=params["thread"])
    except Exception as e:
        connection.close()
        return json.dumps({"code": 1, "response": (e.message)})

    return json.dumps({"code": 0, "response": response})


@app.route("/subscribe/", methods=['POST'])
def subscribe_thread():

    connection = db_tools.connect()

    params = request.json

    try:
        functions.check(params, ["user", "thread"])
        response = thread_tools.subscribe(
            connection=connection, user=params["user"], thread=params["thread"])
    except Exception, e:
        connection.close()
        return json.dumps({"code": 1, "response": (e.message)})

    connection.close()
    return json.dumps({"code": 0, "response": response})


@app.route("/unsubscribe/", methods=['POST'])
def unsubscribe_thread():
    connection = db_tools.connect()

    params = request.json

    try:
        functions.check(params, ["user", "thread"])
        response = thread_tools.unsubscribe(
            connection=connection, user=params["user"], thread=params["thread"])
    except Exception, e:
        connection.close()
        return json.dumps({"code": 1, "response": (e.message)})

    connection.close()
    return json.dumps({"code": 0, "response": response})


@app.route("/open/", methods=['POST'])
def open_thread():

    connection = db_tools.connect()

    params = request.json

    try:
        functions.check(params, ["thread"])
        response = thread_tools.open_close(connection, params["thread"], isClosed=0)
    except Exception as e:
        connection.close()
        return ({"code": 1, "response": (e.message)})

    connection.close()
    return json.dumps({"code": 0, "response": response})


@app.route("/close/", methods=['GET', 'POST'])
def close_thread():

    connection = db_tools.connect()

    params = request.json

    try:
        functions.check(params, ["thread"])
        response = thread_tools.open_close(connection, params["thread"], isClosed=1)
    except Exception as e:
        connection.close()
        return ({"code": 1, "response": (e.message)})

    connection.close()
    return json.dumps({"code": 0, "response": response})


@app.route("/restore/", methods=['POST'])
def restore_thread():

    connection = db_tools.connect()

    params = request.json

    try:
        functions.check(params, ["thread"])
        response = thread_tools.restore_remove(connection, params["thread"], isDeleted=0)
    except Exception as e:
        connection.close()
        return ({"code": 1, "response": (e.message)})

    connection.close()
    return json.dumps({"code": 0, "response": response})


@app.route("/remove/", methods=['GET', 'POST'])
def remove_thread():

    connection = db_tools.connect()

    params = request.json

    try:
        functions.check(params, ["thread"])
        response = thread_tools.restore_remove(connection, params["thread"], isDeleted=1)
    except Exception as e:
        connection.close()
        return ({"code": 1, "response": (e.message)})

    connection.close()
    return json.dumps({"code": 0, "response": response})


@app.route("/listPosts/", methods=["GET"])
def list_posts():
    connection = db_tools.connect()
    params = functions.get_json(request)
    entity = "thread"
    optional = functions.get_optional(
        request=params, values=["limit", "order", "since", "sort"])
    try:
        functions.check(params, ["thread"])
        response = post_tools.posts_list(
            connection=connection, entity="thread", params=optional, identifier=params["thread"], related=[])
    except Exception as e:
        connection.close()
        return json.dumps({"code": 1, "response": (e.message)})
    connection.close()
    return json.dumps({"code": 0, "response": response})


@app.route("/list/", methods=["GET"])
def list_thread():

    connection = db_tools.connect()

    params = functions.get_json(request)

    optional = functions.get_optional(
        request=params, values=["since", "limit", "order"])

    try:
        response = thread_tools.list(connection=connection, required=params,
                               optional=optional, related=[])
    except Exception as e:
        connection.close()
        return json.dumps({"code": 1, "response": (e.message)})

    connection.close()
    return json.dumps({"code": 0, "response": response})
