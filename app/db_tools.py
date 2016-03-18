from DBConfig import *
import MySQLdb as db


def connect():
    return db.connect(host=DB_HOST,
                      user=DB_USER,
                      passwd=DB_PASSWORD,
                      db=DB_NAME,
                      charset=DB_CHARSET)


def execute(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except db.Error:
        connection.rollback()
    cursor.close()
    return