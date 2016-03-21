from app import app
from app.user_api.user_app import app as user_app
from app.forum_api.forum_app import app as forum_app
from app.thread_api.thread_app import app as thread_app

API_PREFIX = "/db/api"

app.register_blueprint(user_app, url_prefix=API_PREFIX + '/user')
app.register_blueprint(forum_app, url_prefix=API_PREFIX + '/forum')
app.register_blueprint(thread_app, url_prefix=API_PREFIX + '/thread')


app.run(host='127.0.0.1', port=8080, debug=True)
