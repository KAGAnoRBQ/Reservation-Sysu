# coding: utf-8
from common.views import login_required_api
from api.form import AddPeriodData, DeleteByIdForm
from flask import request
from common import const, utils
from common.response import reply
from models import PeriodData, ensure_session_removed
from pydash import pick

# @login_required_api
# @ensure_session_removed
def add_period_data():
    print request.form
    form = AddPeriodData(request.form)
    if not form.validate():
        return reply(success=False, message='参数错误', error_code=const.code_param_err)

    period_data = {
        'period_class_id': form.period_class_id.data,
        # 'start_time': form.start_time.data,
        # 'end_time': form.end_time.data,
        'record_status': const.record_normal,
    }
    period_data['period_class_id'] = int(period_data['period_class_id'])
    res = utils.add_by_data(PeriodData, period_data)
    return reply(success=res[0], message=res[1], error_code=res[2])


@login_required_api
@ensure_session_removed
def delete_period_data():
    form = DeleteByIdForm(request.form)
    if not form.validate():
        return reply(success=False, message='参数错误', error_code=const.code_param_err)

    res = utils.delete_by_id(PeriodData, form.id.data)
    return reply(success=res[0], message=res[1], error_code=res[2])

# @login_required_api
def query_period_data():
    period_datas = PeriodData.query.order_by(
        PeriodData.period_class_id
    ).filter_by(
        record_status=const.record_normal
    ).all()
    data = []
    for period_data in period_datas:
        data.append(period_data.to_json())
    return reply(success=True, data=data, message='done', error_code=const.code_success)
