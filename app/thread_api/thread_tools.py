from app.user_api import user_tools
from app.forum_api import forum_tools
from app import db_tools


def create(connection, forum, title, isClosed, user, date, message, slug, optional):

    isDeleted = 0
    if "isDeleted" in optional:
        isDeleted = optional["isDeleted"]

    query = 'INSERT INTO Threads (forum, title, isClosed, user, date, message, slug, isDeleted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    params = (forum, title, isClosed, user, date, message, slug, isDeleted, )

    thread = db_tools.execute_update(connection, query, params)

    if thread == "Error":
        raise Exception("Thread already exists")

    response = {
        'date': str(date),
        'forum': forum,
        'id': thread,
        'isClosed': bool(isClosed),
        'isDeleted': bool(isDeleted),
        'message': message,
        'slug': slug,
        'title': title,
        'user': user,
    }
    return response


def details(connection, id, related):

    query = 'SELECT date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts FROM Threads WHERE id = %s'
    params = (id, )
    thread = db_tools.execute_select(connection, query, params)

    if len(thread) == 0:
        raise Exception('Thread not founded')

    thread = thread[0]
    thread = {
        'date': str(thread[0]),
        'forum': thread[1],
        'id': thread[2],
        'isClosed': bool(thread[3]),
        'isDeleted': bool(thread[4]),
        'message': thread[5],
        'slug': thread[6],
        'title': thread[7],
        'user': thread[8],
        'dislikes': thread[9],
        'likes': thread[10],
        'points': thread[11],
        'posts': thread[12],
    }

    if "user" in related:
        try:
            thread["user"] = user_tools.details(connection, thread["user"])
        except Exception:
            pass

    if "forum" in related:
        try:
            thread["forum"] = forum_tools.details(connection, short_name=thread["forum"], optional=[])
        except Exception:
            pass

    return thread


def vote(connection, vote, thread):
    if vote == -1:
        query = 'UPDATE Threads SET dislikes = dislikes + 1, points = points - 1 WHERE id = %s'
    else:
        query = 'UPDATE Threads SET likes = likes + 1, points = points + 1 WHERE id = %s'

    params = (thread, )

    try:
        db_tools.execute_update(connection, query, params)
    except Exception as e:
        print (e.message)

    return details(connection, id=thread, related=[])


def update(connection, message, slug, thread):
    query = 'UPDATE Threads SET slug = %s, message = %s WHERE id = %s'
    params = (slug, message, thread, )

    try:
        db_tools.execute_update(connection, query, params)
    except Exception as e:
        print (e.message)
    return details(connection, id=thread, related=[])


def subscribe(connection, user, thread):
    query = 'INSERT INTO Subscribe (thread, user) VALUES (%s, %s)'
    params = (thread, user, )
    subscriptions = []
    try:
        db_tools.execute_update(connection, query, params)
    except Exception as e:
        print (e.message)

    query = 'SELECT thread, user FROM Subscribe WHERE thread = %s AND user = %s'

    try:
        subscriptions = db_tools.execute_select(connection, query, params)
    except Exception as e:
        print (e.message)

    result = {"thread": subscriptions[0][0], "user": subscriptions[0][1]}

    return result


def unsubscribe(connection, user, thread):
    query = 'DELETE FROM Subscribe WHERE thread = %s AND user = %s'
    params = (thread, user, )

    try:
        db_tools.execute_update(connection, query, params)
    except Exception as e:
        print (e.message)

    result = {"thread": thread, "user": user}
    return result


def open_close(connection, thread, isClosed):
    query = 'UPDATE Threads SET isClosed = %s WHERE id = %s'
    params = (isClosed, thread, )

    try:
        db_tools.execute_update(connection, query, params)
    except Exception as e:
        print (e.message)

    response = {"thread": thread}

    return response


def restore_remove(connection, thread, isDeleted):
    posts = 0
    current_state = db_tools.execute_select(connection,
        "SELECT isDeleted FROM Threads WHERE id = %s", (thread,))[0][0]


    if current_state != isDeleted:
        if isDeleted == 0:
            query = 'SELECT COUNT(id) FROM Posts WHERE thread = %s'
            params = (thread, )
            posts = db_tools.execute_select(connection, query, params)[0][0]

        query_thread = 'UPDATE Threads SET isDeleted = %s, posts = %s WHERE id = %s'
        query_post = 'UPDATE Posts SET isDeleted = %s WHERE thread = %s'
        params_thread = (isDeleted, posts, thread, )

        try:
            db_tools.execute_update(connection, query_thread, params_thread)
            db_tools.execute_update(connection, query_post, (isDeleted, thread, ))
        except Exception as e:
            print (e.message)

    response = {"thread": thread}

    return response


def inc_posts(connection, post):
    query = 'SELECT thread FROM Posts WHERE id = %s'
    params = (post, )
    thread = db_tools.execute_select(connection, query, params)[0][0]

    query = 'UPDATE Threads SET posts = posts + 1 WHERE id = %s'
    params = (thread, )
    db_tools.execute_update(connection, query, params)

    return


def dec_posts(connection, post):
    query = 'SELECT thread FROM Posts WHERE id = %s'
    params = (post, )
    thread = db_tools.execute_select(connection, query, params)[0][0]

    query = 'UPDATE Threads SET posts = posts - 1 WHERE id = %s'
    params = (thread, )
    db_tools.execute_update(connection, query, params)

    return


def list(connection, required, optional, related):

    query = "SELECT date, dislikes, forum, id, isClosed, isDeleted, likes, message, points, posts, slug, title, user FROM Threads WHERE "
    threads = []

    if 'forum' in required:
        query += "forum = " + "\'" + str(required["forum"][0]) + "\'"
    if 'user' in required:
        query += "user = " + "\'" + str(required["user"][0]) + "\'"

    if 'since' in optional:
        since = optional["since"][0]
        query += " AND date >= " + "\'" + str(since) + "\'"

    if 'order' in optional:
        order = optional["order"][0]
        query += " ORDER BY date " + "".join(optional["order"])

    if 'limit' in optional:
        limit = optional["limit"][0]
        query += " LIMIT " + "".join(optional["limit"])

    try:
        threads = db_tools.execute_select(connection, query, ())
    except Exception as e:
        print (e.message)

    response = []
    if threads != ():
        for thread in threads:
            thread = {
                'date': str(thread[0]),
                'dislikes': thread[1],
                'forum': thread[2],
                'id': thread[3],
                'isClosed': bool(thread[4]),
                'isDeleted': bool(thread[5]),
                'likes': thread[6],
                'message': thread[7],
                'points': thread[8],
                'posts': thread[9],
                'slug': thread[10],
                'title': thread[11],
                'user': thread[12]
            }

            if "user" in related:
                try:
                    thread["user"] = user_tools.details(connection, thread["user"])
                except Exception:
                    pass

            if "forum" in related:
                print thread["forum"]
                thread["forum"] = forum_tools.details(connection, thread["forum"], [])

            response.append(thread)

    return response