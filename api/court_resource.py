# coding: utf-8
from common.views import login_required_api
from api.form import AddCourtResource, DeleteByIdForm
from flask import request
from common import const, utils
from common.response import reply
from models import CourtResource, ensure_session_removed
from models import *


@login_required_api
@ensure_session_removed
def add_court_resource():
    form = AddCourtResource(request.form)
    if not form.validate():
        return reply(success=False, message='参数错误', error_code=const.code_param_err)
    court_resource_exist = CourtResource.query.filter_by(
        date = form.date.data,
        period_id = form.period_id.data,
        court_id = form.court_id.data,
        court_number = form.court_number.data,
        record_status = const.record_normal,
    ).first()
    if court_resource_exist:
        return reply(success=False, message='场地资源已存在', error_code=const.code_param_illegal)
    court_resource = {
        'date': form.date.data,
        'period_id': form.period_id.data,
        'court_id': form.court_id.data,
        'court_number': form.court_number.data,
        'occupied': form.occupied.data,
        'max_order_count': form.max_order_count.data,
        'order_count': form.order_count.data,
    }
    res = utils.add_by_data(CourtResource, court_resource)
    return reply(success=res[0], message=res[1], error_code=res[2])


@login_required_api
@ensure_session_removed
def delete_court_resource():
    form = DeleteByIdForm(request.form)
    if not form.validate():
        return reply(success=False, message='参数错误', error_code=const.code_param_err)

    res = utils.delete_by_id(CourtResource, form.id.data)
    return reply(success=res[0], message=res[1], error_code=res[2])

@login_required_api
def query_court_resource():
    court_resource_id = utils.get_court_resource_id(request)
    court_id = utils.get_court_id(request)
    if court_resource_id is not None:
        court_resources = CourtResource.query.order_by(
            CourtResource.court_id
        ).filter_by(
            id = court_resource_id,
            record_status = const.record_normal
        ).all()
    elif court_id is not None:
        court_resources = CourtResource.query.order_by(
            CourtResource.court_id
        ).filter_by(
            court_id = court_id,
            record_status = const.record_normal
        ).all()
    else:
        court_resources = CourtResource.query.order_by(
            CourtResource.court_id
        ).filter_by(
            record_status = const.record_normal
        ).all()
    data = []
    for court_resource in court_resources:
        data.append(court_resource.to_json())
    return reply(success=True, data=data, message='done', error_code=const.code_success)


@login_required_api
def query_name_by_id():
    court_id = request.args.get('court_id', None)
    gym_id = request.args.get('gym_id', None)
    court = Court.query.filter_by(
        id = court_id,
        record_status = const.record_normal
    ).first()
    gym = Gym.query.filter_by(
        id = gym_id,
        record_status = const.record_normal
    ).first()
    data = {}
    data["court_id"] = court_id
    data["gym_id"] = gym_id
    data["court_name"] = court.court_name
    data["gym_name"] = gym.gym_name
    return reply(success=True, data=data, message='done', error_code=const.code_success)

@login_required_api
def query_field_data():
    courts = Court.query.filter_by(
        record_status = const.record_normal
    ).all()
    data = []
    for court in courts:
        ret = {}
        ret["court_id"] = court.id
        ret["gym_id"] = court.gym_id
        ret["court_name"] = court.court_name
        ret["period_class_id"] = court.period_class_id
        ret["order_days"] = court.order_days
        gym = Gym.query.filter_by(
            id = ret["gym_id"],
            record_status = const.record_normal
        ).first()
        ret["gym_name"] = gym.gym_name
        period_class = PeriodClass.query.filter_by(
            id = ret["period_class_id"],
            record_status = const.record_normal
        ).first()
        ret["period_class_name"] = period_class.period_class_name
        data.append(ret)
    return reply(success=True, data=data, message='done', error_code=const.code_success)
