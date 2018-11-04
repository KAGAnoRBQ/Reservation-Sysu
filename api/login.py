from api.form import LoginForm
from flask import request
from common.utils import param_error
from common.views import auth
from models import UserInfo
from common import const
from flask_login import login_user, current_user
from common.response import reply
import logging


def login():
    form = LoginForm(request.form)
    if not form.validate():
        return param_error(form.errors)
    user = UserInfo.query.filter_by(
        user_number=form.user_number.data,
        record_status=const.record_normal
    ).first()
    if not user or user.password != form.password.data:
        return reply(
            success=False,
            message="用户不存在或密码错误"
        )
    if user.disabled == const.user_disabled_true:
        return reply(
            success=False,
            message="账号被冻结，无法登陆"
        )
    auth.login(user)
    return reply(
        success=True,
        message="登陆成功",
    )


def login_out():
    if current_user.is_authenticated:
        auth.login_out()
    return reply(
        success=True,
    )
