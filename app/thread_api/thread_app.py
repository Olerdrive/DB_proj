from app import app
from flask import jsonify, request, Blueprint
from DBConfig import *
from app import db_tools, functions
import thread_tools
import urlparse
import json

app = Blueprint('thread_app', __name__)