from app import app
from flask import Flask, request
import db_tools as DBTools
from flask import jsonify
from app.db_tools import *


@app.route('/clear/', methods=['GET'])
def clear():
    connection = DBTools.connect()
    tables = ['Users', 'Forums', 'Threads', 'Posts', 'Followers', 'Subscriptions']
    DBTools.execute(connection, "SET global foreign_key_checks = 1;")
    for table in tables:
        query = "TRUNCATE TABLE %s;" % table
        DBTools.execute(connection, query)
    DBTools.execute(connection, "SET global foreign_key_checks = 1;")
    connection.close()
    return jsonify({"code": STATUS_CODE['OK'], "response": 'OK'})