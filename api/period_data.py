# coding: utf-8
from common.views import login_required_api
from api.form import AddPeriodData, DeleteByIdForm
from flask import request
from common import const, utils
from common.response import reply
from models import PeriodData, ensure_session_removed

# @login_required_api
# @ensure_session_removed
def add_period_data():
    form = AddPeriodData(request.form)
    if not form.validate():
        return reply(success=False, message='参数错误', error_code=const.code_param_err)
    period_data_exist = PeriodData.query.filter_by(
        period_class_id=form.period_class_id.data,
        start_time=form.start_time.data,
        end_time=form.end_time.data,
        record_status=const.record_normal,
    ).first()
    if period_data_exist:
        return reply(success=False, message='时间段数据已存在', error_code=const.code_param_illegal)
    period_data = {
        'period_class_id': form.period_class_id.data,
        'start_time': form.start_time.data,
        'end_time': form.end_time.data,
    }
    res = utils.add_by_data(PeriodData, period_data)
    return reply(success=res[0], message=res[1], error_code=res[2])

# @login_required_api
# @ensure_session_removed
def delete_period_data():
    form = DeleteByIdForm(request.form)
    if not form.validate():
        return reply(success=False, message='参数错误', error_code=const.code_param_err)

    res = utils.delete_by_id(PeriodData, form.id.data)
    return reply(success=res[0], message=res[1], error_code=res[2])

# @login_required_api
def query_period_data():
    period_id = utils.get_period_id(request)
    period_class_id = utils.get_real_period_class_id(request)
    if period_id is not None:
        period_datas = PeriodData.query.order_by(
            PeriodData.period_class_id
        ).filter_by(
            id = period_id,
            record_status=const.record_normal
        ).all()
    else:
        period_datas = PeriodData.query.order_by(
            PeriodData.period_class_id
        ).filter_by(
            period_class_id = period_class_id,
            record_status=const.record_normal
        ).all()
    data = []
    for period_data in period_datas:
        data.append(period_data.to_json())
    return reply(success=True, data=data, message='done', error_code=const.code_success)
