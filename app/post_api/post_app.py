from app import app
from flask import jsonify, request, Blueprint
from DBConfig import *
from app import db_tools, functions
import post_tools
from app.forum_api import forum_tools
from app.thread_api import thread_tools
import urlparse
import json

app = Blueprint('post_app', __name__)


@app.route('/create/', methods=['GET', 'POST'])
def post_create():

    connection = db_tools.connect()

    params = request.json

    optional = functions.get_optional(
        params,
        ["parent",
         "isApproved",
         "isHighlighted",
         "isEdited",
         "isSpam",
         "isDeleted"]
    )

    try:
        functions.check(
            params,
            ["date",
             "thread",
             "message",
             "user",
             "forum"]
        )

        response = post_tools.create(connection, params["date"], params["thread"], params[
                               "message"], params["user"], params["forum"], optional)

    except Exception as e:
        connection.close()
        return json.dumps({"code": 3, "response": (e.message)})

    connection.close()
    return json.dumps({"code": 0, "response": response})


@app.route("/details/", methods=["GET"])
def post_details():
    connection = db_tools.connect()
    params = functions.get_json(request)
    required_data = ["post"]
    related = functions.get_related(params)
    try:
        functions.check(params, required_data)
        response = post_tools.details(connection, params["post"], related)
    except Exception as e:
        connection.close()
        return json.dumps({"code": 1, "response": (e.message)})
    connection.close()
    return json.dumps({"code": 0, "response": response})


@app.route("/list/", methods=["GET"])
def post_list():
    connection = db_tools.connect()
    content = functions.get_json(request)
    try:
        identifier = content["forum"]
        entity = "forum"
    except KeyError:
        try:
            identifier = content["thread"]
            entity = "thread"
        except Exception as e:
            connection.close()
            return json.dumps({"code": 1, "response": (e.message)})

    optional = functions.get_optional(
        request=content, values=["limit", "order", "since"])
    try:
        p_list = post_tools.posts_list(
            connection=connection, entity=entity, params=optional, identifier=identifier, related=[])
    except Exception as e:
        connection.close()
        return json.dumps({"code": 1, "response": (e.message)})
    connection.close()
    return json.dumps({"code": 0, "response": p_list})


@app.route("/update/", methods=["POST"])
def post_update():
    connection = db_tools.connect()
    params = request.json
    try:
        functions.check(params, ["post", "message"])
        response = post_tools.update(connection=connection, post=params[
                               "post"], message=params["message"])
    except Exception as e:
        connection.close()
        return json.dumps({"code": 1, "response": (e.message)})
    connection.close()
    return json.dumps({"code": 0, "response": response})


@app.route("/vote/", methods=["POST"])
def post_vote():
    connection = db_tools.connect()
    params = request.json
    try:
        functions.check(params, ["post", "vote"])
        response = post_tools.vote(connection=connection, post=params["post"], vote=params["vote"])
    except Exception as e:
        connection.close()
        return json.dumps({"code": 1, "response": (e.message)})
    connection.close()
    return json.dumps({"code": 0, "response": response})


@app.route("/remove/", methods=["POST"])
def post_remove():
    connection = db_tools.connect()
    params = request.json
    try:
        functions.check(params, ["post"])
        response = post_tools.restore_remove(
            connection=connection, post=params["post"], isDeleted=1)
        #thread_tools.dec_posts(connection, params["post"]) done inside post_tools
    except Exception as e:
        connection.close()
        return json.dumps({"code": 1, "response": (e.message)})
    connection.close()
    return json.dumps({"code": 0, "response": response})


@app.route("/restore/", methods=["POST"])
def post_restore():
    connection = db_tools.connect()
    params = request.json
    try:
        functions.check(params, ["post"])
        response = post_tools.restore_remove(
            connection=connection, post=params["post"], isDeleted=0)
        #thread_tools.inc_posts(connection, params["post"])
    except Exception as e:
        connection.close()
        return json.dumps({"code": 1, "response": (e.message)})
    connection.close()
    return json.dumps({"code": 0, "response": response})