from app.user_api import user_tools
from app.forum_api import forum_tools
from app.thread_api import thread_tools
from app import db_tools


def enlength(str_id):
    while len(str_id) < 7:
        str_id = "0" + str_id[0:]

    return str_id


def serialize_f(post):
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
    query = []
    parameters= []

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

    update_thread_posts = "UPDATE Threads SET posts = posts + 1 WHERE id = %s"

    with connection:
        cursor = connection.cursor()
        cursor.execute(update_thread_posts, (thread, ))
        cursor.execute(query, parameters)
        connection.commit()
        post_id = cursor.lastrowid
        cursor.close()

    post = post_query(connection, post_id)

    set_post_path(connection, post, post_id)


    del post["dislikes"]
    del post["likes"]
    del post["parent"]
    del post["points"]
    return post


def details(connection, details_id, related):
    post = post_query(connection, details_id)

    if post is None:
        raise Exception("no post with id = " + details_id)

    if "user" in related:
        try:
            post["user"] = user_tools.details(connection, post["user"])
        except Exception:
            pass

    if "forum" in related:
        try:
            post["forum"] = forum_tools.details(connection, post["forum"], [])
        except Exception:
            pass

    if "thread" in related:
        try:
            post["thread"] = thread_tools.details(connection, post["thread"], [])
        except Exception:
            pass

    return post


def posts_list(connection, entity, params, identifier, related=[]):
    query = "SELECT * FROM Posts WHERE " + \
                entity + " = " + '\'' + str(''.join(identifier)) + '\''

    sort = 'flat'
    order = 'desc'
    limit = 0

    parameters = tuple()
    if "since" in params:
        query += " AND date >= %s"
        parameters += tuple(params["since"])

    if "sort" in params:
        sort = check_sort(params["sort"][0])

    if "order" in params:
        order = check_order(params["order"][0])

    sort_order_stmt = make_sort_statement(sort, order)
    query += sort_order_stmt

    if "limit" in params:
        limit = int(str(params["limit"][0]))
        query += " LIMIT " + ''.join(params["limit"])

    posts = db_tools.execute_select(connection, query, (parameters))

    if sort != 'flat':
        posts = get_child_posts(connection, posts,sort, limit)

    post_list = []
    for post in posts:
        parent = post[9]
        if post[9] == 0:
            parent = None
        responseDict = {
            'date': str(post[4]),
            'dislikes': post[6],
            'forum': post[3],
            'id': post[0],
            'isApproved': bool(post[12]),
            'isDeleted': bool(post[15]),
            'isEdited': bool(post[13]),
            'isHighlighted': bool(post[11]),
            'isSpam': bool(post[14]),
            'likes': post[7],
            'message': post[5],
            'parent': parent,
            'points': post[8],
            'thread': post[1],
            'user': post[2],
        }

        if "user" in related:
            try:
                responseDict["user"] = user_tools.details(connection, responseDict["user"])
            except Exception:
                pass

        if "forum" in related:
            try:
                responseDict["forum"] = forum_tools.details(connection, responseDict["forum"],[])
            except Exception:
                pass

        if "thread" in related:
            try:
                responseDict["thread"] = thread_tools.details(connection, id=responseDict["thread"], related=[])
            except Exception:
                pass

        post_list.append(responseDict)

    return post_list


def vote(connection, vote, post):
    if vote == 1:
        query = "UPDATE Posts SET likes = likes + 1, points = points + 1 WHERE id = " + \
            str(post)
    else:
        query = "UPDATE Posts SET dislikes = dislikes + 1, points = points - 1 WHERE id = " + \
            str(post)

    db_tools.execute_update(connection, query, ())

    return


def update(connection, post, message):
    query = "UPDATE Posts SET message = %s WHERE id = %s"
    params = (message, post,
              )
    db_tools.execute_update(connection, query, params)
    return details(connection, details_id=post, related=[])


def restore_remove(connection, post, isDeleted):
    current_state = db_tools.execute_select(connection,
        "SELECT isDeleted FROM Posts WHERE id = %s", (post,))[0][0]

    query = "UPDATE Posts SET isDeleted = %s WHERE id = %s"

    params = (isDeleted, post)
    if current_state != isDeleted:
        if isDeleted == 0:
            thread_tools.inc_posts(connection, post)
        else:
            thread_tools.dec_posts(connection, post)

    db_tools.execute_update(connection, query, params)

    response = {"post": post}
    return response


def post_query(connection, id):
    post = db_tools.execute_select(
        connection,
        'SELECT date, dislikes, forum, id, isApproved, isDeleted, isEdited, isHighlighted, isSpam, likes, message, parent, points, thread, user FROM Posts WHERE id = %s ;', (
            id, )
    )

    if len(post) == 0:
        return None

    post = serialize_f(post)
    return post


def make_sort_statement(sort, order):
    stmt = ' ORDER BY date'

    if sort != 'flat':
        stmt = " AND parent is NULL ORDER BY path {}, date DESC"
    else:
        return stmt + " " + order

    return stmt.format(order)


def check_sort(string):
    string = string.lower()

    if string not in ['flat', 'tree', 'parent_tree']:
        string = 'flat'
        raise Exception("Wrong sort type")
    return string


def check_order(string):
    string = string.lower()

    if string not in ['asc', 'desc']:
        string = 'desc'
        raise Exception("Wrong order type")
    return string


def get_child_posts(connection, posts, sort, limit):
    cursor = connection.cursor()

    query = 'SELECT * FROM Posts WHERE LEFT(path, 7) = %s ORDER BY path ASC'

    if sort == 'tree' and limit > 0:
        query += ' LIMIT %s'

    new_posts = []

    for post in posts:
        id = post[0]
        if sort == 'tree':
            params = (enlength(str(id)), limit)
        elif sort == 'parent_tree':
            params = (enlength(str(id)), )

        cursor.execute(query, params)
        child_posts = cursor.fetchall()

        if sort == 'tree':
            limit -= len(child_posts)

        new_posts += child_posts

    return new_posts


def prepare_post(post):
    post[4] = post[4].strftime("%Y-%m-%d %H:%M:%S")


def sort_by_id(post):
    return post[0]


def set_post_path(connection, post, post_id):
    update_path = "UPDATE Posts SET path =  %s WHERE id = %s"
    parent_path = "SELECT path FROM Posts WHERE id = %s"

    if post["parent"] is None:
        path = enlength(str(post_id))
    else:
        parent_path = db_tools.execute_select(connection, parent_path, (post["parent"],))
        path = "".join(parent_path[0]) + "." + enlength(str(post_id))

    db_tools.execute_update(connection, update_path, (path, post_id,))
