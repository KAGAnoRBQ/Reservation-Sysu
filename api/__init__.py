from api.db_test import db_add
from api.login import login, login_out
from api.user import register
from api.department import add_department, delete_department, query_department

__all__ = [
    'db_add',
    'login',
    'login_out',
    'register',
    'add_department',
    'delete_department',
    'query_department',
]
