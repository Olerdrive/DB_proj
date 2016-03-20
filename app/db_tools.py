from DBConfig import *
import MySQLdb as db


def connect():
    return db.connect(host=DB_HOST,
                      user=DB_USER,
                      passwd=DB_PASSWORD,
                      db=DB_NAME,
                      charset=DB_CHARSET)


def execute(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        cursor.close()
    except db.Error:
        connection.rollback()
    return


def execute_update(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        last_id = cursor.lastrowid
        cursor.close()
        return last_id
    except db.Error:
        connection.rollback()
        cursor.close()
        return "Error"



def execute_select(connection, query):
    cursor = connection.cursor()
    result = []
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except db.Error:
        cursor.close()

