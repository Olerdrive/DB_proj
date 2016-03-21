from app import app
from flask import jsonify, request, Blueprint
from DBConfig import *
from app import db_tools, functions
import user_tools
from app.post_api import post_tools
import urlparse
import json

app = Blueprint('user_app', __name__)


@app.route('/create/', methods=['POST'])
def create_user():

    connection = db_tools.connect()
    params = request.json

    optional = functions.get_optional(params, values=["isAnonymous"])

    try:
        functions.check(params, ["username", "about", "name", "email"])
        userr = user_tools.create(connection, params["username"], params["about"],
                                  params["name"], params["email"], optional)
    except Exception as e:
        if e.message == "5":
            connection.close()
            return jsonify({"code": 5, "response": (e.message)})
        connection.close()
        return jsonify({"code": 1, "response": (e.message)})
    connection.close()
    return jsonify({"code": 0, "response": userr})


@app.route('/details/', methods=['GET'])
def details():

    connection = db_tools.connect()
    params = functions.get_json(request)

    try:
        functions.check(params, ["user"])
        userr = user_tools.details(connection, params["user"][0])
    except Exception as e:
        connection.close()
        return jsonify({"code": 1, "response": e.message})

    connection.close()
    return jsonify({"code": 0, "response": userr})


@app.route('/follow/', methods=['POST'])
def follow():

    connection = db_tools.connect()
    params = request.json

    try:
        functions.check(params, ["follower", "followee"])
        response = user_tools.follow(connection=connection, email1=params[
                               "follower"], email2=params["followee"])
    except Exception as e:
        connection.close()
        return json.dumps({"code": 1, "response": (e.message)})

    connection.close()
    return json.dumps({"code": 0, "response": response})


@app.route('/unfollow/', methods=['POST'])
def unfollow():
    connection = db_tools.connect()
    params = request.json

    try:
        functions.check(params, ["follower", "followee"])
        response = user_tools.unfollow(connection=connection, email1=params[
                                 "follower"], email2=params["followee"])
    except Exception as e:
        connection.close()
        return json.dumps({"code": 1, "response": (e.message)})

    connection.close()
    return json.dumps({"code": 0, "response": response})


@app.route('/updateProfile/', methods=['POST'])
def update_profile():
    connection = db_tools.connect()
    params = request.json

    try:
        functions.check(params, ["about", "user", "name"])
        response = user_tools.update_profile(connection=connection, about=params["about"], user_email=params[
                                      "user"], name=params["name"])

    except Exception as e:
        connection.close()
        return json.dumps({"code": 1, "response": (e.message)})
    connection.close()
    return json.dumps({"code": 0, "response": response})


@app.route('/listFollowers/', methods=['GET'])
def list_followers():

    connection = db_tools.connect()

    params = functions.get_json(request)

    optional = functions.get_optional(params, ["limit", "order", "since_id"])

    try:
        functions.check(params, ["user"])
        response = user_tools.list_followers(connection, params["user"], optional)
    except Exception as e:
        connection.close()
        return json.dumps({"code": 1, "response": (e.message)})
    connection.close()
    return json.dumps({"code": 0, "response": response})


@app.route('/listFollowing/', methods=['GET'])
def list_followees():

    connection = db_tools.connect()

    params = functions.get_json(request)

    optional = functions.get_optional(params, ["limit", "order", "since_id"])

    try:
        functions.check(params, ["user"])
        response = user_tools.list_followees(connection, params["user"], optional)
    except Exception as e:
        connection.close()
        return json.dumps({"code": 1, "response": (e.message)})
    connection.close()
    return json.dumps({"code": 0, "response": response})


@app.route('//listPosts/', methods=['GET'])
def user_listPosts():

    connection = db_tools.connect()

    params = functions.get_json(request)

    optional = functions.get_optional(params, ["limit", "order", "since"])

    try:
        functions.check(params, ["user"])
        response = post_tools.posts_list(
            connection=connection, entity="user", params=optional, identifier=params["user"], related=[])
    except Exception as e:
        connection.close()
        return json.dumps({"code": 1, "response": (e.message)})
    connection.close()
    return json.dumps({"code": 0, "response": response})