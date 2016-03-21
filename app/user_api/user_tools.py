from app import db_tools


def create(connection, username, about, name, email, optional):
    isAnonymous = 0
    if "isAnonymous" in optional:
        isAnonymous = optional["isAnonymous"]
    query = 'INSERT INTO Users (username, about, name, email, isAnonymous) VALUES ("{0}", "{1}", "{2}", "{3}", {4})'.format (
        username, about, name, email, isAnonymous)

    inserted_id = db_tools.execute_update(connection, query)
    if inserted_id == "Error":
        raise Exception("5")

    user = {
        'about': about,
        'email': email,
        'id': inserted_id,
        'isAnonymous': bool(isAnonymous),
        'name': name,
        'username': username
    }

    return user


def details(connection, user_email):
    query = 'SELECT id, email, about, isAnonymous, name, username FROM Users WHERE email = "%s"' % user_email
    user = db_tools.execute_select(connection, query)

    if len(user) == 0:
        raise Exception("User not found")

    user = serialize_u(user)

    query = 'SELECT followee FROM Follow WHERE follower = "%s"' % user_email
    following = db_tools.execute_select(connection, query)
    user["following"] = to_list(following)


    query ='SELECT follower FROM Follow WHERE followee = "%s"' % user_email
    followers = db_tools.execute_select(connection,query)
    user["followers"] = to_list(followers)

    query = 'SELECT thread FROM Subscribe WHERE user = "%s"' % user_email
    subscriptions = db_tools.execute_select(connection, query)
    user["subscriptions"] = to_list(subscriptions)


    return user


def follow(connection, email1, email2):
    query = 'INSERT INTO Follow (follower, followee) VALUES ("%s", "%s")' % (email1, email2)
    response = db_tools.execute_update(connection, query)

    return details(connection, email1)


def unfollow(connection, email1, email2):

    query = 'DELETE FROM Follow WHERE follower = "{}" AND followee = "{}"'.format(email1, email2)
    response = db_tools.execute_update(connection, query)

    return details(connection, email1)


def update_profile(connection, about, user_email, name):
    query = 'UPDATE Users SET about = "{}", name = "{}" WHERE email = "{}"'.format(about, name, user_email)
    response = db_tools.execute_update(connection, query)

    return details(connection, user_email)


def list_subsriptions(connection, user_email):
    query = 'SELECT thread FROM Subscribe WHERE user = "%s"' % str(user_email[0])
    subscriptions = db_tools.execute_select(connection, query)

    response = []

    if len(subscriptions) == 0:
        return response

    for sub in subscriptions:
        response.append(str(sub))

    return response


def list_followers(connection, user_email, optional):
    query = 'SELECT follower FROM Follow WHERE followee = "{}"'.format(str(user_email[0]))
    response = []

    if len(optional) != 0:
        if 'since_id' in optional:
            query += " AND id >= " + optional['since_id'][0]

        if 'order' in optional:
            query += " ORDER BY followee " + optional['order'][0]

        if 'limit' in optional:
            query += " LIMIT " + optional['limit'][0]

    followers = db_tools.execute_select(connection, query)
    if len(followers) == 0:
        return response

    for follower in followers:
        response.append(details(connection, str(follower[0])))

    return response


def list_followees(connection, user_email, optional):
    query = 'SELECT followee FROM Follow WHERE follower = "%s"' % str(user_email[0])
    response = []
    print query
    if len(optional) != 0:
        if 'since_id' in optional:
            query += " AND id >= " + optional['since_id'][0]

        if 'order' in optional:
            query += " ORDER BY followee " + optional["order"][0]

        if 'limit' in optional:
            query += " LIMIT " + optional["limit"][0]

    followees = db_tools.execute_select(connection, query)
    print followees
    if len(followees) == 0:
        return response

    for followee in followees:
        print str(followee[0])
        response.append(details(connection, str(followee[0])))

    return response


def list_posts(connection, user_email, optional):
    query = 'SELECT date, dislikes, forum, id, isApproved, isDeleted, isEdited, isHighlighted, isSpam, likes, ' \
                    'message, parent, points, thread, user FROM Posts WHERE user = "{}"'.format(str(user_email[0]))

    if 'since' in optional:
        query += " AND date >= " + "\'" + optional['since'][0] + "\'"

    if 'order' in optional:
        query += " ORDER BY date " + "".join(optional["order"][0])

    if 'limit' in optional:
        query += " LIMIT " + "".join(optional["limit"][0])

    posts = db_tools.execute_select(connection, query)

    if len(posts) != 0:
        posts = posts[0]
        posts = {
            'date': posts[0].strftime("%Y-%m-%d %H:%M:%S"),
            'dislikes': posts[1],
            'forum': posts[2],
            'id': posts[3],
            'isApproved': posts[4],
            'isDeleted': posts[5],
            'isEdited': posts[6],
            'isHighlighted': posts[7],
            'isSpam': posts[8],
            'likes': posts[9],
            'message': posts[10],
            'parent': posts[11],
            'points': posts[12],
            'thread': posts[13],
            'user': posts[14]
        }

    return posts


def to_list(array):
    lst = []
    if array is None:
        return lst
    for obj in array:
        lst.append(obj[0])
    return lst


def serialize_u(user):
    user = user[0]
    response = {
        'about': user[2],
        'email': user[1],
        'id': user[0],
        'isAnonymous': bool(user[3]),
        'name': user[4],
        'username': user[5]
    }
    return response
