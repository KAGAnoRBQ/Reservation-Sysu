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
import datetime
import re

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



@login_required_api
def selectCourt():
    courts = Court.query.all()
    if not courts:
        return reply(success=False, message='无任何场馆！',error_code=1)

    gyms = [Gym.query.filter_by(id=court.gym_id).first() for court in courts]
    if not gyms:
        return reply(success=False, message='数据错误！',error_code=2)

    sc = [{'court_id':court.id, 'gym_name':gym.gym_name, 'court_name':court.court_name, 'court_type':court.court_type, 'court_fee':court.court_fee, 'gym_id':gym.id} for court, gym in zip(courts, gyms)]
    data = {'src' : sc}
    
    return reply(success=True, data=data, error_code='')

@login_required_api
def ordering(id):
    admin = 0
    if current_user.user_type == const.user_type_admin:
        admin = 1

    court = Court.query.filter_by(id=id).first()
    if not court:
        return reply(success=False, message='无对应场馆！',error_code=1)

    date_now = datetime.date.today()

    dates = []
    occupy = {}
    periods = [(per.id, per.start_time, per.end_time) for per in PeriodData.query.filter_by(period_class_id=court.period_class_id).all()]
    periods = [(period[0], period[1].strftime('%H:%M'), period[2].strftime('%H:%M')) for period in periods]             
    if not periods:
        return reply(success=False, message='无对应时间段！',error_code=2)


    for i in range(1, court.order_days+1):
        date = (date_now+datetime.timedelta(days = i))
        d = date.strftime('%m.%d')
        dates.append(d)
        occupy[d] = {}
        for period in periods:
            occupy[d][period[0]]={}
            court_resource = CourtResource.query.filter_by(date=date, period_id=period[0], court_id=id).all()
            if not court_resource:
                return reply(success=False, message='无场地资源！',error_code=3)
            for cr in court_resource:
                if cr.occupied :
                    occupy[d][period[0]][cr.court_number] = 1
                else :
                    if cr.order_count < cr.max_order_count:
                        occupy[d][period[0]][cr.court_number] = 0
                    else:
                        occupy[d][period[0]][cr.court_number] = 2

    data = {
        'court_id' : id,
        'dates': dates,
        'periods': periods, 
        'occupy': occupy, 
        'admin': admin
    }
    return reply(success=True, data=data, error_code='')
                    

@login_required_api
def order_submit(id):
    court = Court.query.filter_by(id=id).first()
    if not court:
        return reply(success=False, message='无对应场馆！',error_code=1)

    date_now = datetime.date.today()

    dates = []
    for i in range(1, court.order_days+1):
        date = (date_now+datetime.timedelta(days = i))
        dates.append(date)

    cr_name = request.args.get('date_period_number')
    pattern = re.compile('(.*)_(.*)_(.*)')
    target_date, target_period, target_number = re.findall(pattern, cr_name)[0]
    target_date = (list(filter(lambda x:  x.strftime('%m.%d')==target_date, dates)))[0]
    
    court_resource_query =CourtResource.query.filter_by(date=target_date, period_id=target_period, court_number=target_number, court_id=id) 
    court_resource = court_resource_query.first()
    if not court_resource :
        return reply(success=False, message="无对应场地资源！", error_code=4)
    if court_resource.order_count<court_resource.max_order_count and not court_resource.occupied:
        cr_data = {
        	'order_count' : court_resource.order_count+1,
     	}
        schedule_query = Schedule.query.filter_by(court_id = id, date = court_resource.date)
        schedule = schedule_query.first()
        if not schedule:
            return reply(success=False, message="数据错误！", error_code=5)
        schedule_date = {
            'order_count' : schedule.order_count+1,
        }
        dt = datetime.datetime.today()
        if dt.microsecond >= 500000:
            dt = dt+ datetime.timedelta(seconds = 1)
        dt = dt - datetime.timedelta(microseconds=dt.microsecond)
        co_data = {
            'id' : None,
            'user_id' : current_user.id,
            'order_time' : dt,
            'resource_id' : court_resource.id,
            'pay_time' : None,
            'amount' : 0,
            'is_acked' : False,
            'ack_time' : None,
            'is_canceled' : False,
            'cancel_time' : None,
            'is_used' : False 
        }
        update_by_data(court_resource_query, cr_data, False)
        update_by_data(schedule_query, schedule_date, False)
        res = add_by_data(CourtOrder, co_data)
        if res[0] is True:
            order_id = CourtOrder.query.filter_by(user_id=current_user.id, order_time=dt, resource_id=court_resource.id, amount=0, \
                                                is_acked=False, is_canceled=False, is_used=False).first()
            if not order_id :
                return reply(success=False, message="数据错误！", error_code=8)
            order_id = order_id.id
            return reply(success=True, data={'order_id': order_id}, error_code=0)
        return reply(success=res[0], message=res[1], error_code=res[2])
    elif court_resource.order_count>=court_resource.max_order_count:
        return reply(success=False, message="当前场地预订剩余量为0！", error_code = 6)
    elif court_resource.occupied:
        return reply(success=False, message="当前场地已占用！", error_code = 7)
    

@login_required_api
def courtResource_cancel(id):
    if current_user.user_type != const.user_type_admin:
        return reply(success=False, message='无权限', error_code=const.code_not_permit)
    
    court = Court.query.filter_by(id=id).first()
    date_now = datetime.date.today()
    dates = []
    for i in range(1, court.order_days+1):
        date = (date_now+datetime.timedelta(days = i))
        dates.append(date)

    pattern = re.compile('(.*)_(.*)_(.*)')
    cr_name = request.args.get('date_period_number')
    target_date, target_period, target_number = re.findall(pattern, cr_name)[0]
    target_date = (list(filter(lambda x:  x.strftime('%m.%d')==target_date, dates)))[0]
    court_resource_query = CourtResource.query.filter_by(date=target_date, period_id=target_period, court_number=target_number, court_id=id)
    court_resource = court_resource_query.first()
    if court_resource and court_resource.occupied == True:
        cr_data = {
            'occupied' : False,
        }
        schedule_query = Schedule.query.filter_by(court_id = id, date = court_resource.date)
        schedule = schedule_query.first()
        if not schedule:
            return reply(success=False, message="数据错误！", error_code=2)
        schedule_date = {
            'occupied_count' : schedule.occupied_count-1,
        }
        update_by_data(court_resource_query, cr_data, False)
        res = update_by_data(schedule_query, schedule_date)
        return reply(success=res[0], message=res[1], error_code=res[2])
    return reply(success=True, message='', error_code=const.success)
    

@login_required_api
def courtResource_occupied(id):
    if current_user.user_type != const.user_type_admin:
        return reply(success=False, message='无权限', error_code=const.code_not_permit)
    
    court = Court.query.filter_by(id=id).first()
    date_now = datetime.date.today()
    dates = []
    for i in range(1, court.order_days+1):
        date = (date_now+datetime.timedelta(days = i))
        dates.append(date)

    pattern = re.compile('(.*)_(.*)_(.*)')
    cr_name = request.args.get('date_period_number')
    target_date, target_period, target_number = re.findall(pattern, cr_name)[0]
    target_date = (list(filter(lambda x:  x.strftime('%m.%d')==target_date, dates)))[0]
    court_resource_query = CourtResource.query.filter_by(date=target_date, period_id=target_period, court_number=target_number, court_id=id)
    court_resource = court_resource_query.first()
    if court_resource and court_resource.occupied == False:
        cr_data = {
            'occupied' : True,
        }
    
        schedule_query = Schedule.query.filter_by(court_id = id, date = court_resource.date)
        schedule = Schedule.query.filter_by(court_id = id, date = court_resource.date).first()
        if not schedule:
            return reply(success=False, message="数据错误！", error_code=2)
        schedule_date = {
            'occupied_count' : schedule.occupied_count+1,
        }
        update_by_data(court_resource_query, cr_data, False)
        res = update_by_data(schedule_query, schedule_date)
        return reply(success=res[0], message=res[1], error_code=res[2])
    return reply(success=True, message='', error_code=const.success)

