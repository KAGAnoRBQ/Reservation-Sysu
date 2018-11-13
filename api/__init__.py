from api.db_test import db_add
from api.login import login, login_out
from api.user import register, change_permission, change_disable, query_user
from api.department import add_department, delete_department, query_department
from api.period_data import add_period_data, delete_period_data, query_period_data
from api.gym import gym_add, query_gym, edit_gym

__all__ = [
    'db_add',
    'login',
    'login_out',
    'register',
    'query_user',
    'change_permission',
    'change_disable',
    'add_department',
    'delete_department',
    'query_department',
    'add_period_data',
    'delete_period_data',
    'query_period_data'
    'gym_add',
    'query_gym',
    'edit_gym',
]
