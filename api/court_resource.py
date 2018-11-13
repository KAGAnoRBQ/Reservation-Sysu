# coding: utf-8
from common.views import login_required_api
from api.form import AddPeriodData, DeleteByIdForm
from flask import request
from common import const, utils
from common.response import reply
from models import CourtResource, ensure_session_removed
from pydash import pick


@login_required_api
@ensure_session_removed
def add_court_resource():
    form = AddCourtResource(request.form)
    if not form.validate():
        return reply(success=False, message='参数错误', error_code=const.code_param_err)

    court_resource = {
        'source_id' = form.source_id.data,
        'date' = form.date.data,
        'period_id' = form.period_id.data,
        'court_id' = form.court_id.data,
        'court_number' = form.court_number.data,
        'occupied' = form.occupied.data,
        'max_order_court' = form.max_order_court.data,
        'order_count' = form.order_count.data,
        'record_status': const.record_normal,
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
    court_resources = CourtResource.query.order_by(
        CourtResource.court_id
    ).filter_by(
        record_status=const.record_normal
    ).all()
    data = []
    for court_resource in court_resources:
        data.append(court_resource.to_json())
    return reply(success=True, data=data, message='done', error_code=const.code_success)