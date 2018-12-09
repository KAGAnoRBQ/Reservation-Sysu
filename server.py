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
        return super(IndexRule, self).match(path='|/', method=method)


def init():
    db.init_app(app)
    db.app = app
    db.create_all()

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
    app.add_url_rule('/user/query2/', 'user_query2', view_func=api.query_user2, methods=['GET'])
    
    # department
    app.add_url_rule('/department/add/', 'department_add', view_func=api.add_department, methods=['POST'])
    app.add_url_rule('/department/delete/', 'department_delete', view_func=api.delete_department, methods=['POST'])
    app.add_url_rule('/department/query/', 'department_query', view_func=api.query_department, methods=['GET'])

    # booking
    app.add_url_rule('/pay/pay_money/', 'money_pay', view_func=api.pay_money, methods=['POST'])
    app.add_url_rule('/my_order/cancel/', 'order_cancel_button', view_func=api.order_cancel_button, methods=['POST'])
    app.add_url_rule('/order/get_info/', 'info_get', view_func=api.get_order_info, methods=['GET'])
    app.add_url_rule('/booking/selectCourt', endpoint='selectCourt', view_func=api.selectCourt, methods=['GET'])
    app.add_url_rule('/booking/order/<id>', endpoint='ordering', view_func=api.ordering, methods=['GET'])
    app.add_url_rule('/booking/orderSubmit/<id>', endpoint='orderSubmit', view_func=api.order_submit, methods=['GET'])
    app.add_url_rule('/booking/resourceCancel/<id>', endpoint='resourceCancel', view_func=api.courtResource_cancel, methods=['GET'])
    app.add_url_rule('/booking/resourceOccupy/<id>', endpoint='resourceOccupy', view_func=api.courtResource_occupied, methods=['GET'])

    # time
    app.add_url_rule('/period_data/add/', 'add_period_data', view_func=api.add_period_data, methods=['POST'])
    app.add_url_rule('/period_data/delete/', 'delete_period_data', view_func=api.delete_period_data, methods=['POST'])
    app.add_url_rule('/period_data/query/', 'query_period_data', view_func=api.query_period_data, methods=['GET'])
    # app.add_url_rule('/period_data/query/', 'query_period_data', view_func=api.query_period_data, methods=['POST'])
    
    # court_resource
    app.add_url_rule('/court_resource/add/', 'add_court_resource', view_func=api.add_court_resource, methods=['POST'])
    app.add_url_rule('/court_resource/delete/', 'delete_court_resource', view_func=api.delete_court_resource,
                     methods=['POST'])
    app.add_url_rule('/court_resource/query/', 'query_court_resource', view_func=api.query_court_resource,
                     methods=['GET'])
    app.add_url_rule('/court_resource/query_name_by_id/', 'query_name_by_id', view_func=api.query_name_by_id,
                     methods=['GET'])
                     
    # schedule
    app.add_url_rule('/schedule/add/', 'add_schedule', view_func=api.add_schedule, methods=['POST'])
    app.add_url_rule('/schedule/delete/', 'delete_schedule', view_func=api.delete_schedule, methods=['POST'])
    app.add_url_rule('/schedule/query/', 'query_schedule', view_func=api.query_schedule, methods=['GET'])

    # gym
    app.add_url_rule('/gym/add/', 'gym_add', view_func=api.gym_add, methods=['POST'])
    app.add_url_rule('/gym/query/', 'gym_query', view_func=api.query_gym, methods=['POST'])
    app.add_url_rule('/gym/edit/', 'gym_edit', view_func=api.edit_gym, methods=['POST'])

    # order
    app.add_url_rule('/order/user_query/', 'order_user_query', view_func=api.order_user_query, methods=['GET'])
    app.add_url_rule('/order/manager_query/', 'order_manager_query', view_func=api.order_manager_query, methods=['GET'])
    app.add_url_rule('/order/cancel/', 'order_cancel', view_func=api.order_cancel, methods=['POST'])

    # account
    app.add_url_rule('/account/user_query/', 'account_user_query', view_func=api.account_user_query, methods=['GET'])
    app.add_url_rule('/account/manager_query/', 'account_manager_query', view_func=api.account_manager_query, methods=['GET'])
    app.add_url_rule('/account/deposit/', 'account_deposit', view_func=api.account_deposit, methods=['POST'])
    app.add_url_rule('/account/query_balance/', 'account_query_balance', view_func=api.account_query_balance, methods=['GET'])
    app.add_url_rule('/account/clear/', 'account_clear', view_func=api.account_clear_balance, methods=['POST'])
    
    #fields
    app.add_url_rule('/sportsfield/define/', 'sportsfield_field_define', view_func=api.sportsfield_define, methods=['GET'])
    app.add_url_rule('/sportsfield/add/', 'sportsfield_field_add', view_func=api.sportsfield_add, methods=['POST'])
    app.add_url_rule('/sportsfield/edit', 'sportsfield_field_edit', view_func=api.sportsfield_edit,methods=['POST'])
    app.add_url_rule('/sportsfield/typequery','sportsfield_court_type_query',view_func=api.court_type_query,methods=['GET'])
    app.add_url_rule('/sportsfield/delete','sportsfield_delete',view_func=api.sportsfield_delete,methods=['GET'])

    #time
    app.add_url_rule('/period/period_query', 'period_period_query', view_func=api.period_query,methods=['GET'])
    app.add_url_rule('/peroid/period_add', 'period_period_add', view_func=api.period_add,methods=['POST'])
    app.add_url_rule('/peroid/peroid_edit', 'period_period_edit', view_func=api.period_edit,methods=['POST'])
    app.add_url_rule('/peroid/period_delete', 'period_delete', view_func=api.period_delete,methods=['GET'])
init()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
