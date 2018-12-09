# coding: utf-8
from common.views import login_required_api
from api.form import AddShcedule, DeleteByIdForm
from flask import request
from common import const, utils
from common.response import reply
from models import Schedule, ensure_session_removed
from models import *

# @login_required_api
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
    }
    res = utils.add_by_data(Schedule, schedule)
    return reply(success=res[0], message=res[1], error_code=res[2])


# @login_required_api
@ensure_session_removed
def delete_schedule():
    form = DeleteByIdForm(request.form)
    if not form.validate():
        return reply(success=False, message='参数错误', error_code=const.code_param_err)

    res = utils.delete_by_id(Schedule, form.id.data)
    return reply(success=res[0], message=res[1], error_code=res[2])

# @login_required_api
def query_schedule():
    schedule_id = utils.get_schedule_id(request)
    court_id = utils.get_court_id(request)
    print ("schedule_id:", schedule_id)
    print ("court_id", court_id)
    if schedule_id is not None:
        schedules = Schedule.query.order_by(
            Schedule.court_id
        ).filter_by(
            id = schedule_id,
            record_status=const.record_normal
        ).all()
    elif court_id is not None:
        schedules = Schedule.query.order_by(
            Schedule.court_id
        ).filter_by(
            court_id = court_id,
            record_status=const.record_normal
        ).all()  
    else:
        schedules = Schedule.query.order_by(
            Schedule.court_id
        ).filter_by(
            record_status=const.record_normal
        ).all()  
    data = []
    for schedule in schedules:
        data.append(schedule.to_json())
    for tmp in data:
        court_id = tmp["court_id"]
        court = Court.query.filter_by(
            id = court_id,
            record_status = const.record_normal
        ).first()
        if court is None:
            continue
        court_name = court.court_name
        gym_id = court.gym_id
        gym = Gym.query.filter_by(
            id = gym_id,
            record_status = const.record_normal
        ).first()
        if gym is None:
            continue
        gym_name = gym.gym_name
        tmp.pop("court_id")
        tmp["court_name"] = court_name
        tmp["gym_name"] = gym_name
    return reply(success=True, data=data, message='done', error_code=const.code_success)
