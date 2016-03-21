from app import app
from flask import Flask, request
import db_tools
from flask import jsonify
from app.db_tools import *


@app.route('/db/api/clear/', methods=['GET', 'POST'])
def clear():
    connection = db_tools.connect()
    tables = ['Users', 'Forums', 'Threads', 'Posts', 'Follow', 'Subscribe']
    db_tools.execute(connection, "SET global foreign_key_checks = 1;")
    for table in tables:
        query = "TRUNCATE TABLE %s;" % table
        db_tools.execute(connection, query)
    db_tools.execute(connection, "SET global foreign_key_checks = 1;")
    connection.close()
    return jsonify({"code": STATUS_CODE['OK'], "response": 'OK'})


@app.route('/db/api/status/', methods=['GET'])
def status():

    connection = connect()
    response = []
    tables = ['Users', 'Threads', 'Forums', 'Posts']

    for table in tables:
        currCount = len(db_tools.execute_select(
            connection, 'SELECT id FROM ' + table, ()))
        response.append(currCount)

    Response = {
        'user': response[0],
        'thread': response[1],
        'forum': response[2],
        'post': response[3]
    }

    connection.close()

    returnResp = Response

    return jsonify({"code": STATUS_CODE['OK'], "response": returnResp})