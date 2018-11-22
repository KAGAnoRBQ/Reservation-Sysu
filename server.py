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

    # db.app = app
    # db.create_all()

    def __(_, resp):
        resp('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Not Found']

    # @login_required_api
    def index():
        search = UserInfo.query.filter_by(
            id='16'
        ).first()
        print(search.user_name)
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
    app.add_url_rule('/user/register/', 'user_register', view_func=api.register, methods=['POST'])
    # department
    app.add_url_rule('/department/add/', 'department_add', view_func=api.add_department, methods=['POST'])
    app.add_url_rule('/department/delete/', 'department_delete', view_func=api.delete_department, methods=['POST'])
    app.add_url_rule('/department/query/', 'department_query', view_func=api.query_department, methods=['GET'])

    # booking
    app.add_url_rule('/pay/pay_money/', 'money_pay', view_func=api.pay_money, methods=['POST'])
    app.add_url_rule('/order/cancel/', 'order_cancel', view_func=api.cancel_order, methods=['POST'])
    app.add_url_rule('/order/get_info/', 'info_get', view_func=api.get_order_info, methods=['GET'])
    app.add_url_rule('/mytest/', 'mytest', view_func=api.mytest, methods=['GET'])


init()

if __name__ == '__main__':
    app.run(debug=True)  # host='0.0.0.0', port=8080, debug=True)
