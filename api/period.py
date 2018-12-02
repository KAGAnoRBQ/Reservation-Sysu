# coding: utf-8
from models import *
from common.views import login_required_api
from flask_login import current_user
from common.response import reply
from api.form import *
from flask import request
from common.utils import *


@login_required_api
@ensure_session_removed
def period_query():
    cur_user = UserInfo.query.filter_by(
        id=current_user.id,
        record_status = const.record_normal
    ).first()
    if not cur_user:
        return reply(success=False, message='内部出错，请联系管理员', error_code=const.code_inner_err)
    if cur_user.user_type > const.user_type_admin:
        return reply(success=False, message='无权限', error_code=const.code_not_permit)

    period_types = PeriodClass.query.order_by(PeriodClass.id).all()
    data = []
    for item in period_types:
        data.append(item.to_json())
    return reply(success=True,data=data,message='done',error_code=const.code_success)


def period_add():
    form = AddPeriodForm(request.form)
    if not form.validate():
        return param_error(form.errors)
    cur_user = UserInfo.query.filter_by(
        id=current_user.id,
        record_status=const.record_normal
    ).first()
    if not cur_user:
        return reply(success=False, message='内部出错，请联系管理员', error_code=const.code_inner_err)
    period_class_name = form.period_class_name.data
    description = form.period_description.data
    print(description)
    if period_class_name:
        period_class_data = {
            "period_class_name":period_class_name,
            "period_class_description":description
        }
        res = add_by_data(PeriodClass,period_class_data)
        return reply(success=res[0], message=res[1], error_code=res[2])
    else:
        return reply(success=False, message="period_class_name required",error_code=const.code_param_err)


def period_edit():
    form = EditPeriodForm(request.form)
    if not form.validate():
        return param_error(form.errors)
    cur_user = UserInfo.query.filter_by(
        id=current_user.id,
        record_status=const.record_normal
    ).first()
    if not cur_user:
        return reply(success=False, message='内部出错，请联系管理员', error_code=const.code_inner_err)
    period_class_id = form.period_id.data
    period_class_data = PeriodClass.query.filter_by(
        id = period_class_id
    )
    period_class_exist = period_class_data.first()
    if period_class_exist:
        update_data ={}
        if form.period_class_name.data and form.period_class_name.data != period_class_exist.period_class_name:
            update_data['period_class_name'] = form.period_class_name.data
        if form.period_description.data and form.period_description.data !=period_class_exist.period_class_description:
            update_data['period_class_description'] = form.period_description.data
        res = update_by_data(period_class_data, update_data, True)
        return reply(success=res[0], message=res[1], error_code=res[2])
    else:
        return reply(success=False, message='找不该时间段类型', error_code=const.code_param_illegal)


def period_delete():
    cur_user = UserInfo.query.filter_by(
        id=current_user.id,
        record_status=const.record_normal
    ).first()
    if not cur_user:
        return reply(success=False, message='内部出错，请联系管理员', error_code=const.code_inner_err)
    period_class_id = get_period_class_id(request)
    period_class_data = PeriodClass.query.filter_by(
        id = period_class_id,
        record_status = const.record_normal
    )
    period_class_exist = period_class_data.first()
    if not period_class_exist:
        return reply(success=False, message='找不该时间段类型', error_code=const.code_param_illegal)
    else:
        res = delete_by_id(PeriodClass, period_class_id)
        return reply(success=res[0], message=res[1], error_code=res[2])
