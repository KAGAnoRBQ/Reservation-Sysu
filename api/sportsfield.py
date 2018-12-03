# coding: utf-8
from models import *
from common.views import login_required_api
from api.form import *
from flask import request
from common.utils import param_error, get_gym_id, update_by_data,add_by_data,get_sportsfield_id,delete_by_id
from common.response import reply
from pydash import pick
from flask_login import current_user


def transform(field):
    sportsfield_data = pick(field,
                            'id',
                            'court_name',
                            'description',
                            'court_type',
                            'court_count',
                            'court_fee',
                            'period_class_id',
                            'order_days')
    period_class_id = sportsfield_data['period_class_id']
    period_class_name = PeriodClass.query.filter_by(
        id=period_class_id
    ).first()
    sportsfield_data['period_class_name'] = period_class_name.period_class_name
    return sportsfield_data

@login_required_api
@ensure_session_removed
def sportsfield_define():
    form = SportFieldDefineForm(request.form)
    if not form.validate():
        return param_error(form.errors)
    gym_id = get_gym_id(request)
    gym = Gym.query.filter_by(
        id = gym_id,
        record_status=const.record_normal
    ).first()
    gym_name = gym.gym_name
    location = gym.location
    sportsfield = Court.query.filter_by(
        gym_id = gym_id,
        record_status = const.record_normal
    ).all()


    reply_data = list(map(lambda x:transform(x), sportsfield))
    for item in reply_data:
        item['gym_name'] = gym_name
        item['location'] = location

    return reply(success=True,data=reply_data, message='done', error_code=const.code_success)


@login_required_api
@ensure_session_removed
def sportsfield_edit():
    form = EditSportFieldForm(request.form)
    if not form.validate():
        return param_error(form.errors)
    court_rel = Court.query.filter_by(
        id=form.id.data,#请求数据：场地id
        record_status=const.record_normal
    )
    court = court_rel.first()
    if not court:
        return reply(success=False, message='找不该运动场', error_code=const.code_param_illegal)
    gym_id = court.gym_id
    gym_rel = Gym.query.filter_by(
        id = gym_id,
        record_status = const.record_normal
    ).first()
    cur_user = UserInfo.query.filter_by(
        id=current_user.id,
        record_status=const.record_normal
    ).first()
    if cur_user.user_type > const.user_type_manage and cur_user.user_number != gym_rel.manager_number:
        return reply(success=False, message='无权限', error_code=const.code_not_permit)
    update_data = {}
    if form.court_name.data and form.court_name.data !=court.court_name:
        update_data['court_name'] = form.court_name.data
    if form.court_type.data and form.court_type.data != court.court_type:
        update_data['court_type'] = form.court_type.data
    if form.court_num.data and form.court_num.data != court.court_count:
        update_data['court_count'] = form.court_num.data
    if form.court_fee.data and form.court_fee.data != court.court_fee:
        update_data['court_fee'] = form.court_fee
    if form.order_days.data and form.order_days.data != court.order_days:
        update_data['order_days'] = form.order_days.data
    if form.court_description.data and form.court_description.data != court.description:
        update_data['description'] = form.court_description.data
    if form.period_class_id.data and form.period_class_id.data != court.period_class_id:
        update_data['period_class_id'] = form.period_class_id
    res = update_by_data(court_rel, update_data,True)
    return reply(success=res[0], message=res[1], error_code=res[2])


@login_required_api
@ensure_session_removed
def sportsfield_add():
    form = AddSportFieldForm(request.form)
    if not form.validate():
        return param_error(form.errors)
    cur_user = UserInfo.query.filter_by(
        id=current_user.id,
        record_status = const.record_normal
    ).first()
    if not cur_user:
        return reply(success=False, message='内部出错，请联系管理员', error_code=const.code_inner_err)
    gym_id = form.gym_id.data
    gym_rel = Gym.query.filter_by(
        id=gym_id,
        record_status=const.record_normal
    )
    if cur_user.user_type > const.user_type_manage and cur_user.user_number != gym_rel.manager_number:
        return reply(success=False, message='无权限', error_code=const.code_not_permit)
    court_data = {
        "gym_id":gym_id,
        "court_name":form.court_name.data,
        "description":form.court_description.data,
        "court_type":form.court_type.data,
        "court_count":form.court_num.data,
        "court_fee":form.court_num.data,
        "order_days":form.order_days.data,
        "period_class_id":form.period_class_id.data
    }
    res = add_by_data(Court,court_data)
    return reply(success=res[0], message=res[1], error_code=res[2])


@login_required_api
@ensure_session_removed
def court_type_query():
    court_type = CourtType.query.order_by(CourtType.id).all()
    data = []
    for court in court_type:
        data.append(court.to_json())
    return reply(success=True,data=data,message='done',error_code=const.code_success)


@login_required_api
@ensure_session_removed
def sportsfield_delete():
    cur_user = UserInfo.query.filter_by(
        id=current_user.id,
        record_status = const.record_normal
    ).first()
    if not cur_user:
        return reply(success=False, message='内部出错，请联系管理员', error_code=const.code_inner_err)
    court_id = get_sportsfield_id(request)
    if not court_id:
        return reply(success=False, message='未知运动场场地', error_code=const.code_param_err)
    court_exits = Court.query.filter_by(
        id = court_id,
        record_status = const.record_normal
    ).first()
    if not court_exits:
        return reply(success=False, message='找不到该运动场地',error_code=const.code_unknown_err)
    res = delete_by_id(Court,court_id)
    return reply(success=res[0],message=res[1],error_code=res[2])


