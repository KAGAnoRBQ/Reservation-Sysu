from api.form import LoginForm
from flask import request
from common.utils import param_error
from common.views import auth
from models import User
from common import const
from common.views import login_required_api
from flask_login import login_user, current_user
import logging


def login():
    form = LoginForm(request.form)
    if not form.validate():
        return param_error(form.errors)
    user = User.query.filter_by(
        username=form.username.data,
        record_status=const.Normal
    ).first()
    if not user or user.password != form.password.data:
        return dict(
            success=False
        )
    auth.login(user)
    return dict(
        success=True
    )


def login_out():
    if current_user.is_authenticated:
        auth.login_out()
    return dict(
        success=True
    )
