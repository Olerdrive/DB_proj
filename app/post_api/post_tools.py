from app.user_api import user_tools
from app.forum_api import forum_tools
from app.thread_api import thread_tools
from app import db_tools


def serialize(post):
    post = post[0]
    response = {
        'date': str(post[0]),
        'dislikes': post[1],
        'forum': post[2],
        'id': post[3],
        'isApproved': bool(post[4]),
        'isDeleted': bool(post[5]),
        'isEdited': bool(post[6]),
        'isHighlighted': bool(post[7]),
        'isSpam': bool(post[8]),
        'likes': post[9],
        'message': post[10],
        'parent': post[11],
        'points': post[12],
        'thread': post[13],
        'user': post[14],
    }
    return response


def create(connection, date, thread, message, user, forum, optional):

    try:
        query = "INSERT INTO Posts (message, user, forum, thread, date"
        values = "(%s, %s, %s, %s, %s"
        parameters = [message, user, forum, thread, date]

        for param in optional:
            query += ", " + param
            values += ", %s"
            parameters.append(optional[param])
    except Exception as e:
        print (e.message)
    query += ") VALUES " + values + ")"
    update_thread_posts = "UPDATE thread SET posts = posts + 1 WHERE id = %s"
    update_parent = "UPDATE post SET parent =  %s WHERE id = %s"
    with connection:
        cursor = connection.cursor()
        cursor.execute(update_thread_posts, (thread, ))
        cursor.execute(query, parameters)
        connection.commit()
        post_id = cursor.lastrowid
        cursor.close()

    post = post_query(connection, post_id)
    del post["dislikes"]
    del post["likes"]
    del post["parent"]
    del post["points"]
    return post