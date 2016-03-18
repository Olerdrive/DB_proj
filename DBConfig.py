DB_USER = "db_user"
DB_PASSWORD = "db_pass"
DB_NAME = "projdb"
DB_CHARSET = "utf8"
DB_HOST = "localhost"

STATUS_CODE = {
    'OK': {'status_code': 0},
    'NOT_FOUND': {'status_code': 1, 'error': 'object not found'},
    'INVALID_REQUEST': {'status_code': 2, 'error': 'invalid request'},
    'WRONG_REQUEST': {'status_code': 3, 'error': 'wrong request'},
    'UNKNOWN_ERROR': {'status_code': 4, 'error': 'unknown error'},
    'ALREADY_EXISTS': {'status_code': 5, 'error': 'object already exists'}
}