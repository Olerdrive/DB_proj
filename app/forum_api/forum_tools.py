from app import db_tools
from app.user_api import user_tools

def serialize_f(forum):
    forum = forum[0]
    response = {
        'id': forum[0],
        'name': forum[1],
        'short_name': forum[2],
        'user': forum[3]
    }

    return response


def create(connection, name, short_name, user):
    query = 'INSERT INTO Forums (name, short_name, user) VALUES ("%s", "%s", "%s")' % \
                                                        (str(name), str(short_name), str(user))

    print query
    inserted_id = db_tools.execute_update(connection, query)
    if inserted_id=="Error":
        raise Exception("5")

    response = {
        'id': inserted_id,
        'name': name,
        'short_name': short_name,
        'user': user
    }

    return response


def details(connection, short_name, optional):
    query = 'SELECT id, name, short_name, user FROM Forums WHERE short_name = "%s"' % str(short_name[0])

    forum = db_tools.execute_select(connection, query)

    if len(forum) == 0:
        raise Exception("Forum not found")

    forum = serialize_f(forum)

    if "user" in optional:
        forum["user"] = user_tools.details(connection, forum["user"])

    return forum


def list_users(connection, short_name, optional):
    query = 'SELECT user.id, user.name, user.email FROM Users " \
        "WHERE user.email IN (SELECT DISTINCT user FROM Posts WHERE forum = "%s"' % str(short_name)
    response = []

    if len(optional) != 0:
        if "since_id" in optional:
            query += " AND users.id >= " + str(optional["since_id"][0])
        if "order" in optional:
            query += " ORDER BY user.name " + str(optional["order"][0])
        if "limit" in optional:
            query += " LIMIT " + str(optional["limit"][0])

    posts = db_tools.execute_select(connection, query)

    if posts is None or len(posts) == 0:
        return response

    for post in posts:
        res = user_tools.details(connection, str(post[2]))
        response.append(res)

    return response
