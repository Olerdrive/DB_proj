from app import app
from app.user_api.user_app import app as user_app

API_PREFIX = "/db/api"

app.register_blueprint(user_app, url_prefix=API_PREFIX + '/user')

app.run(host='127.0.0.1', port=8080, debug=True)
