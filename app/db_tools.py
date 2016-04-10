from DBConfig import *
import MySQLdb as db


def connect():
    return db.connect(host=DB_HOST,
                      user=DB_USER,
                      passwd=DB_PASSWORD,
                      db=DB_NAME,
                      charset=DB_CHARSET,
                      use_unicode=True)


def execute(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        cursor.close()
    except db.Error:
        connection.rollback()
    return


def execute_update(connection, query, params):
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        inserted_id = cursor.lastrowid
        connection.commit()
        cursor.close()
    except db.Error:
        connection.rollback()
        cursor.close()
        return "Error"
    return inserted_id


def execute_select(connection, query, params):
    result = []
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
    except db.Error as e:
        result = None
        cursor.close()
    return result

