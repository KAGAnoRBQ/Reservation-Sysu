# -*- coding: utf-8 -*-

from api.form import *
from models import *
from common import const, utils
from common.utils import param_error
from common.response import *
from common.views import login_required_api
from flask import request
from pydash import pick
from flask_login import current_user
import logging


def get_user_order(order):
    court_resource = CourtResource.query.filter(CourtResource.id == order.resource_id).first()
    court = Court.query.filter(Court.id == court_resource.court_id).first()
    period_data = PeriodData.query.filter(PeriodData.id == court_resource.period_id).first()
    gym = Gym.query.filter(Gym.id == court.gym_id).first()
    item = {
        'order_id': order.id,
        'gym_name': gym.gym_name,
        'court_name': court.court_name,
        'order_time': order.order_time,
        'court_number': court_resource.court_number,
        'date': court_resource.date,
        'start_time': str(period_data.start_time),
        'end_time': str(period_data.end_time),
        'amount': order.amount
    }

    if order.is_canceled:
        item['state'] = 'canceled'
    elif order.is_used:
        item['state'] = 'used'
    elif order.is_acked:
        item['state'] = 'acked'
    else:
        item['state'] = 'normal'

    return item


def get_manager_order(order):
    user = UserInfo.query.filter(UserInfo.id == order.user_id).first()
    court_resource = CourtResource.query.filter(CourtResource.id == order.resource_id).first()
    court = Court.query.filter(Court.id == court_resource.court_id).first()
    period_data = PeriodData.query.filter(PeriodData.id == court_resource.period_id).first()
    gym = Gym.query.filter(Gym.id == court.gym_id).first()
    item = {
        'order_id': order.id,
        'dept_id': user.dept_id,
        'user_name': user.user_name,
        'user_number': user.user_number,
        'gym_name': gym.gym_name,
        'court_name': court.court_name,
        'order_time': order.order_time,
        'court_number': court_resource.court_number,
        'date': court_resource.date,
        'start_time': str(period_data.start_time),
        'end_time': str(period_data.end_time),
        'amount': order.amount
    }

    if order.is_canceled:
        item['state'] = 'canceled'
    elif order.is_used:
        item['state'] = 'used'
    elif order.is_acked:
        item['state'] = 'acked'
    else:
        item['state'] = 'normal'

    return item


@login_required_api
def order_user_query():
    current_page, page_size = utils.get_page_info(request)

    orders = db.session.query(CourtOrder).filter(CourtOrder.user_id == current_user.id)
    total_count = orders.count()
    orders = orders.paginate(current_page, page_size, False).items
    print(orders)
    orders = map(lambda order: get_user_order(order), orders)
    orders = list(orders)
    return query_reply(success=True,
                       data={'orders': orders},
                       paging={
                           'current': current_page,
                           'pages': int((total_count - 1) / page_size + 1),
                           'records': total_count,
                       },
                       message='done', error_code=const.code_success)


@login_required_api
def order_manager_query():
    if current_user.user_type != const.user_type_manage:
        return reply(success=False, message='无权限', error_code=const.code_not_permit)

    current_page, page_size = utils.get_page_info(request)
    orders = db.session.query(CourtOrder)
    total_count = orders.count()
    orders = orders.paginate(current_page, page_size, False).items
    print(orders)
    orders = map(lambda order: get_manager_order(order), orders)
    orders = list(orders)
    return query_reply(success=True,
                       data={'orders': orders},
                       paging={
                           'current': current_page,
                           'pages': int((total_count - 1) / page_size + 1),
                           'records': total_count,
                       },
                       message='done', error_code=const.code_success)


@login_required_api
@ensure_session_removed
def order_cancel():
    order_id = request.form.get('order_id')
    order = CourtOrder.query.filter(CourtOrder.id == order_id)
    order_rel = order.first()

    if not order_rel:
        return reply(success=False, message='非法订单号', error_code=const.code_param_illegal)
    if order_rel.user_id != current_user.id:
        return reply(success=False, message='无权限', error_code=const.code_not_permit)
    if order_rel.is_canceled:
        return reply(success=False, message='订单已取消', error_code=const.code_param_illegal)
    if order_rel.is_acked or order_rel.is_used:
        return reply(success=False, message='订单已生效，无法取消', error_code=const.code_param_illegal)
    account = Account(user_id=order_rel.user_id, order_id=order_id, account_summary='退款', account_time=datetime.now(),
                      amount=order_rel.amount)
    db.session.add(account)
    users = UserInfo.query.filter_by(id=order_rel.user_id).first()
    users.account_balance += order_rel.amount
    update_data = {
        'is_canceled': 1,
        'cancel_time': datetime.now()
    }

    res = utils.update_by_data(order, update_data, True)
    return reply(success=res[0], message=res[1], error_code=res[2])
