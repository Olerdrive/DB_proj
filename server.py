from app import app
from app.user_api.user_app import app as user_app
from app.forum_api.forum_app import app as forum_app
from app.thread_api.thread_app import app as thread_app
from app.post_api.post_app import app as post_app

API_PREFIX = "/db/api"

app.register_blueprint(user_app, url_prefix=API_PREFIX + '/user')
app.register_blueprint(forum_app, url_prefix=API_PREFIX + '/forum')
app.register_blueprint(thread_app, url_prefix=API_PREFIX + '/thread')
app.register_blueprint(post_app, url_prefix=API_PREFIX + '/post')


app.run(host='0.0.0.0', port=8000, debug=False)
