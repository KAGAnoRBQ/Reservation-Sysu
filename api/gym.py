# coding: utf-8
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


@login_required_api
@ensure_session_removed
def gym_add():
    form = AddGymForm(request.form)
    if not form.validate():
        return param_error(form.errors)
    cur_user = UserInfo.query.filter_by(
        id=current_user.id,
        record_status=const.record_normal
    ).first()
    if not cur_user:
        return reply(success=False, message='内部出错，请联系管理员', error_code=const.code_inner_err)
    if cur_user.user_type != const.user_type_admin:
        return reply(success=False, message='无权限', error_code=const.code_not_permit)
    gym_exist = Gym.query.filter_by(
        gym_name=form.gym_name.data,
        record_status=const.record_normal
    ).first()
    if gym_exist:
        return reply(success=False, message='该体育馆已存在', error_code=const.code_param_illegal)
    manager = UserInfo.query.filter_by(
        user_number=form.manager_number.data,
        record_status=const.record_normal
    ).first()
    if not manager:
        return reply(success=False, message='非法管理员职工号', error_code=const.code_param_illegal)
    if manager.user_type > const.user_type_manage:
        return reply(success=False, message='该职工没有管理权限，请先将其升为管理员', error_code=const.code_param_illegal)
    gym_data = {
        'gym_name': form.gym_name.data,
        'location': form.location.data,
        'manager_number': form.manager_number.data,
    }
    res = utils.add_by_data(Gym, gym_data)
    return reply(success=res[0], message=res[1], error_code=res[2])


def transform(gym):
    item = pick(gym,
                'id',
                'gym_name',
                'location',
                'manager_number',
                )
    manager = UserInfo.query.filter_by(
        record_status=const.record_normal,
        user_number=gym.manager_number,
    ).first()
    item['manager_name'] = manager.user_name
    return item


@login_required_api
@ensure_session_removed
def query_gym():
    form = QueryGymForm(request.form)
    if not form.validate():
        return param_error(form.errors)
    cur_user = UserInfo.query.filter_by(
        id=current_user.id,
        record_status=const.record_normal
    ).first()
    gyms = Gym.query.filter_by(
        record_status=const.record_normal
    )
    if cur_user.user_type > const.user_type_admin:
        gyms = gyms.filter_by(
            manager_number=cur_user.user_number,
        )
    gym_query = dict()
    if form.gym_name.data:
        gym_query['gym_name'] = form.gym_name.data
    if form.location.data:
        gym_query['location'] = form.location.data
    if form.manager_number.data:
        gym_query['manager_number'] = form.manager_number.data
    if gym_query:
        gyms = gyms.filter_by(
            **gym_query
        )
    gyms = gyms.all()
    data = map(lambda x: transform(x), gyms)
    data = list(data)
    return reply(success=True,
                 data=data,
                 message='done', error_code=const.code_success)


@login_required_api
@ensure_session_removed
def edit_gym():
    form = EditGymForm(request.form)
    if not form.validate():
        return param_error(form.errors)
    gym = Gym.query.filter_by(
        id=form.id.data,
        record_status=const.record_normal
    )
    gym_rel = gym.first()
    if not gym_rel:
        return reply(success=False, message='找不到该体育馆', error_code=const.code_param_illegal)
    cur_user = UserInfo.query.filter_by(
        id=current_user.id,
        record_status=const.record_normal
    ).first()
    if cur_user.user_type != const.user_type_admin and cur_user.user_number != gym_rel.manager_number:
        return reply(success=False, message='无权限', error_code=const.code_not_permit)
    update_data = {}
    if form.gym_name.data and form.gym_name.data != gym_rel.gym_name:
        update_data['gym_name'] = form.gym_name.data
    if form.location.data and form.location.data != gym_rel.location:
        update_data['location'] = form.location.data
    if cur_user.user_type == const.user_type_admin and form.manager_number.data != gym_rel.manager_number:
        manager = UserInfo.query.filter_by(
            user_number=form.manager_number.data,
            record_status=const.record_normal
        ).first()
        if not manager:
            return reply(success=False, message='非法管理员职工号', error_code=const.code_param_illegal)
        if manager.user_type > const.user_type_manage:
            return reply(success=False, message='该职工没有管理权限，请先将其升为管理员', error_code=const.code_param_illegal)
        update_data['manager_number'] = form.manager_number.data
    res = utils.update_by_data(gym, update_data, True)
    return reply(success=res[0], message=res[1], error_code=res[2])
