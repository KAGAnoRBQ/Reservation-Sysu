# coding: utf-8
# Code by Barron Pun
from flask import request
from api.form import PayOrder, CancelOrder
from common.utils import param_error
from models import *
from common.response import reply
from common.views import login_required_api
from common.utils import add_by_data, update_by_data
import time
import random

'''
付款
error_code description:
    1: 订单不存在
    2: 订单已经付过款了
    3: 余额不足
    4: 付款失败，其它错误
    5: 要求付款的订单已经被取消了
'''


@login_required_api
@ensure_session_removed
def pay_money():
    # Method: Post
    # The parameter received from the user's form is order's id
    form = PayOrder(request.form)
    if not form.validate():
        return param_error(form.errors())
    user_order = CourtOrder.query.filter_by(
        id=form.order_id.data
    ).first()

    if not user_order:
        return reply(success=False, message='There is no such order!',error_code=1)

    # line 21-31 查找订单对应的场地的表，查出单价
    resource_id = user_order.resource_id
    court_resource = CourtResource.query.filter_by(
        id=resource_id
    ).first()
    if not court_resource:
        return reply(success=False, message='Failed payment!', error_code=4)

    if court_resource.is_canceled == 1:
        return reply(success=False, message='This order has been canceled', error_code=5)

    court_id = court_resource.court_id

    court_info = Court.query.filter_by(
        id=court_id
    ).first()
    if not court_info:
        reply(success=False, message='Failed payment', error_code=4)

    order_price = court_info.court_fee
    paid = user_order.amount  # 该订单已经付了多少钱

    # If the order has been paid, then false is returned
    if paid > 0:
        return reply(success=False, message='This order has been paid!', error_code=2)

    user_id = user_order.user_id  # 该订单所属用户的id
    user_info = UserInfo.query.filter_by(
        id=user_id
    ).first()
    if not user_info:
        reply(success=False, message='Failed payment', error_code=4)
    left_balance = user_info.account_balance  # 用户的当前余额

    if order_price > left_balance:
        return reply(success=False, message="Insufficient remaining balance!", error_code=3)

    # 下面进行付款并修改数据库中相应的表单
    # 1. 修改user_order
    '''
    order_update = {
        'pay_time': datetime.now(),
        'amount': order_price
    }
    user_order = CourtOrder.query.filter_by(
        id=form.order_id.data
    )
    user_order.update(**order_update) # update 唔可以用，唔知点解, update要query对象才能用，加了first之后不能用
    '''
    user_order.pay_time = datetime.now()
    user_order.amount = order_price

    # 2. 修改user_info中的用户余额
    user_info.account_balance = left_balance - order_price

    # 3、记账，修改Account表单
    account_data = {
        'user_id': user_id,
        'order_id': form.order_id.data,
        'account_summary': '扣款',
        'account_time': datetime.now(),
        'amount': order_price
    }
    res = add_by_data(Account, account_data) # 前面的修改在add_by_data 这里一同commit了

    return reply(success=res[0], message=res[1], error_code=res[2])


'''
取消订单
error_code description:
    1: 订单不存在
    2: 订单已经被取消过了
    3: 其它错误
'''


@login_required_api
@ensure_session_removed
def order_cancel_button():
    # Method: post
    form = CancelOrder(request.form)
    if not form.validate():
        return param_error(form.errors())
    user_order = CourtOrder.query.filter_by(
        id=form.cancel_order_id.data
    ).first()  # 要取消的用户订单表单

    if not user_order:
        return reply(success=False, message='There is no such order!', error_code=1)
    is_canceled = user_order.is_canceled
    if is_canceled:
        return reply(success=False, message="This order has been canceled!", error_code=2)

    money_paid = user_order.amount  # 已经付款的金额

    if money_paid == 0:  # 还未付款，直接取消即可，不用返回钱款
        user_order.is_canceled = True  # 登记取消
        user_order.cancel_time = datetime.now()  # 登记取消时间

        # 场地资源 + 1
        court_resource = CourtResource.query.filter_by(
            id=user_order.resource_id
        )
        if not court_resource:
            return reply(success=False, message='Failed to cancel!', error_code=3)
        court_resource.order_count += 1

        # 记账
        user_id = user_order.user_id
        account_data = {
            'user_id': user_id,
            'order_id': form.order_id.data,
            'account_summary': '退款',
            'account_time': datetime.now(),
            'amount': 0
        }
        res = add_by_data(Account, account_data)  # 上面修改一起commit

        if not res[0]:
            return reply(success=False, message='Failed to cancel!', error_code=3)

        return reply(success=res[0], message='Order canceled successfully!', error_code=const.code_success)

    elif money_paid > 0:  # 已经付过款，要返回钱款
        user_order.is_canceled = True  # 记录取消
        user_order.cancel_time = datetime.now()  # 记录取消时间

        # 获取订单单价
        resource_id = user_order.resource_id
        court_resource = CourtResource.query.filter_by(
            id=resource_id
        ).first()
        if not court_resource:
            return reply(success=False, message='Failed to cancel!', error_code=3)
        court_id = court_resource.court_id
        court_info = Court.query.filter_by(
            id=court_id
        ).first()
        if not court_info:
            return reply(success=False, message='Failed to cancel!', error_code=3)
        order_price = court_info.court_fee
        # 返回钱款给用户
        user_id = user_order.user_id
        user_info = UserInfo.query.filter_by(
            id=user_id
        ).first()
        if not user_info:
            return reply(success=False, message='Failed to cancel!', error_code=3)
        user_info.account_balance = user_info.account_balance + order_price

        # 场地资源 + 1
        court_resource.order_count += 1

        # 记账
        account_data = {
            'user_id': user_id,
            'order_id': form.cancel_order_id.data,
            'account_summary': '退款',
            'account_time': datetime.now(),
            'amount': order_price
        }
        res = add_by_data(Account, account_data)  # 前面的修改一起commit

        if not res[0]:
            return reply(success=False, message='Failed to cancel!', error_code=3)

        return reply(success=res[0], message='Order canceled successfully!', error_code=const.code_success)


def get_order_info():
    # method: get
    order_id = request.args.get('order_id')
    order_table = CourtOrder.query.filter_by(
        id=order_id
    ).first()
    if not order_table:
        return reply(success=False, message="There is no such order!", error_code=1)

    resource_info = CourtResource.query.filter_by(
        id=order_table.resource_id
    ).first()
    court_info = Court.query.filter_by(
        id=resource_info.court_id
    ).first()
    period_info = PeriodData.query.filter_by(
        id=resource_info.period_id
    ).first()
    gym_info = Gym.query.filter_by(
        id=court_info.gym_id
    ).first()

    data = {
        'order_time': order_table.order_time,
        'pay_time': order_table.pay_time,
        'paid_money': order_table.amount,
        'is_canceled': order_table.is_canceled,
        'cancel_time': order_table.cancel_time,
        'gym_name': gym_info.gym_name,
        'gym_location': gym_info.location,
        'court_type': court_info.court_type,
        'order_price': court_info.court_fee,
        'start_time': str(period_info.start_time),
        'end_time': str(period_info.end_time),
        'court_number': resource_info.court_number
    }

    return reply(success=True, data=data, message="")