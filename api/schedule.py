# coding: utf-8
from common.views import login_required_api
from api.form import AddShcedule, DeleteByIdForm
from flask import request
from common import const, utils
from common.response import reply
from models import Schedule, ensure_session_removed
from pydash import pick


@login_required_api
@ensure_session_removed
def add_schedule():
    form = AddShcedule(request.form)
    if not form.validate():
        return reply(success=False, message='参数错误', error_code=const.code_param_err)

    schedule = {
        'court_id': form.court_id.data,
        'date': form.date.data,
        'total': form.total.data,
        'order_count': form.order_count.data,
        'occupied_count': form.occupied_count.data,
        'visible': form.visible.data,
        'enabled': form.enabled.data,
        'record_status': const.record_normal,
    }
    res = utils.add_by_data(Schedule, schedule)
    return reply(success=res[0], message=res[1], error_code=res[2])


@login_required_api
@ensure_session_removed
def delete_schedule():
    form = DeleteByIdForm(request.form)
    if not form.validate():
        return reply(success=False, message='参数错误', error_code=const.code_param_err)

    res = utils.delete_by_id(Schedule, form.id.data)
    return reply(success=res[0], message=res[1], error_code=res[2])

@login_required_api
def query_schedule():
    schedules = Schedule.query.order_by(
        Schedule.court_id
    ).filter_by(
        record_status=const.record_normal
    ).all()
    data = []
    for schedule in schedules:
        data.append(schedule.to_json())
    return reply(success=True, data=data, message='done', error_code=const.code_success)
