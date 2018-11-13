# coding: utf-8
from flask import render_template
from werkzeug.wsgi import DispatcherMiddleware
from app import app
from werkzeug.routing import Rule
import api
from models import db
from flask_login import LoginManager
from models import UserInfo
from common.views import login_required_api

class IndexRule(Rule):
    def match(self, path, method=None):
        if path.startswith('|/api/'):
            return
        if path.startswith('|/static/'):
            return
        return super().match(path='|/', method=method)

def init():
    db.init_app(app)

    def __(_, resp):
        resp('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Not Found']

    @login_required_api
    def index():
        return render_template('index.html')

    app.wsgi_app = DispatcherMiddleware(__, {'/api': app.wsgi_app})
    login_manager = LoginManager(app)
    login_manager.user_callback = lambda user_id: UserInfo.query.filter(UserInfo.id == user_id).first()

    app.add_url_rule(IndexRule('/', endpoint='index'), view_func=index)

    # test
    app.add_url_rule('/db_test/', 'api_db_test', view_func=api.db_add, methods=['GET'])
    # login
    app.add_url_rule('/user/login/', 'user_login', view_func=api.login, methods=['POST'])
    app.add_url_rule('/user/login_out/', 'user_login_out', view_func=api.login_out, methods=['POST'])
    # user
    app.add_url_rule('/user/register/', 'user_register', view_func=api.register, methods=['POST'])
    app.add_url_rule('/user/query/', 'user_query', view_func=api.query_user, methods=['POST'])
    app.add_url_rule('/user/permission/change/', 'user_permission_change', view_func=api.change_permission,
                     methods=['POST'])
    app.add_url_rule('/user/disable/change/', 'user_disable_change', view_func=api.change_disable,
                     methods=['POST'])

    # department
    app.add_url_rule('/department/add/', 'department_add', view_func=api.add_department, methods=['POST'])
    app.add_url_rule('/department/delete/', 'department_delete', view_func=api.delete_department, methods=['POST'])
    app.add_url_rule('/department/query/', 'department_query', view_func=api.query_department, methods=['GET'])

    # court_resource
    app.add_url_rule('/court_resource/add/', 'add_court_resource', view_func=api.add_court_resource, methods=['POST'])
    app.add_url_rule('/court_resource/delete/', 'delete_court_resource', view_func=api.delete_court_resource, methods=['POST'])
    app.add_url_rule('/court_resource/query/', 'query_court_resource', view_func=api.query_court_resource, methods=['POST'])

    # time
    app.add_url_rule('/period_data/add/', 'add_period_data', view_func=api.add_period_data, methods=['POST'])
    app.add_url_rule('/period_data/delete/', 'delete_period_data', view_func=api.delete_period_data, methods=['POST'])
    app.add_url_rule('/period_data/query/', 'query_period_data', view_func=api.query_period_data, methods=['POST'])

    # gym
    app.add_url_rule('/gym/add/', 'gym_add', view_func=api.gym_add, methods=['POST'])
    app.add_url_rule('/gym/query/', 'gym_query', view_func=api.query_gym, methods=['POST'])
    app.add_url_rule('/gym/edit/', 'gym_edit', view_func=api.edit_gym, methods=['POST'])

init()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
