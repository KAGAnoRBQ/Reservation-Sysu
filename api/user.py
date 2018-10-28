from api.form import RegisterForm
from models import *
from common import const, utils
from common.utils import param_error
from common.response import reply
from common.views import login_required_api
from flask import request
import logging


@login_required_api
@ensure_session_removed
def register():
    form = RegisterForm(request.form)
    if not form.validate():
        return param_error(form.errors)
    user_exist = UserInfo.query.filter_by(
        user_name=form.user_name.data,
        record_status=const.record_normal
    ).first()
    if user_exist:
        return reply(success=False, message='用户名已存在', error_code=const.code_param_illegal)
    dept_exist = Department.query.filter_by(
        id=form.dept_id.data,
        record_status=const.record_normal
    ).first()
    if not dept_exist:
        logging.info('right way')
        return reply(success=False, message='部门不存在', error_code=const.code_param_illegal)
    user_data = {
        'user_name': form.user_name.data,
        'user_alias': form.user_alias.data,
        'user_number': form.user_number.data,
        'dept_id': form.dept_id.data,
        'password': form.password.data,
        'user_type': const.user_type_normal,
        'account_balance': 0,
        'disabled': const.user_disabled_false,
    }
    res = utils.add_by_data(UserInfo, user_data)
    return reply(success=res[0], message=res[1], error_code=res[2])
