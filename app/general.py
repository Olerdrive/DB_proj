from app import app
from flask import Flask, request
from flask import jsonify

from app.db_tools import *

@app.route('/clear/', methods=['GET'])
def clear():
	connection = connect()
