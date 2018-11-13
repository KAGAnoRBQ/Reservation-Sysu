from api.form import *
from models import *
from common import const, utils
from common.utils import param_error
from common.response import *
from common.views import login_required_api
from flask import request
from pydash import pick
from flask_login import current_user
import logging


@ensure_session_removed
def register():
    form = RegisterForm(request.form)
    if not form.validate():
        return param_error(form.errors)
    user_exist = UserInfo.query.filter_by(
        user_alias=form.user_alias.data,
        record_status=const.record_normal
    ).first()
    if user_exist:
        return reply(success=False, message='用户别名已存在', error_code=const.code_param_illegal)
    user_exist = UserInfo.query.filter_by(
        user_number=form.user_number.data,
        record_status=const.record_normal
    ).first()
    if user_exist:
        return reply(success=False, message='职工号已存在', error_code=const.code_param_illegal)
    dept_exist = Department.query.filter_by(
        id=form.dept_id.data,
        record_status=const.record_normal
    ).first()
    if not dept_exist:
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


@login_required_api
@ensure_session_removed
def change_permission():
    form = ChangePermissionForm(request.form)
    if not form.validate():
        return param_error(form.errors)
    cur_user = UserInfo.query.filter_by(
        id=current_user.id,
        record_status=const.record_normal
    ).first()
    if not cur_user:
        return reply(success=False, message='内部出错，请联系管理员', error_code=const.code_inner_err)
    change_user = UserInfo.query.filter_by(
        id=form.user_id.data,
        record_status=const.record_normal
    )
    rel_change_user = change_user.first()
    if not rel_change_user:
        return reply(success=False, message='要修改的用户不存在', error_code=const.code_param_illegal)
    min_level = min(rel_change_user.user_type, int(form.user_type.data))
    if cur_user.user_type >= min_level:
        return reply(success=False, message='无权限', error_code=const.code_not_permit)
    update_data = dict()
    update_data['user_type'] = form.user_type.data
    res = utils.update_by_data(change_user, update_data, True)
    return reply(success=res[0], message=res[1], error_code=res[2])


@login_required_api
@ensure_session_removed
def change_disable():
    form = ChangeDisableForm(request.form)
    if not form.validate():
        return param_error(form.errors)
    cur_user = UserInfo.query.filter_by(
        id=current_user.id,
        record_status=const.record_normal
    ).first()
    if not cur_user:
        return reply(success=False, message='内部出错，请联系管理员', error_code=const.code_inner_err)
    change_user = UserInfo.query.filter_by(
        id=form.user_id.data,
        record_status=const.record_normal
    )
    rel_change_user = change_user.first()
    if not rel_change_user:
        return reply(success=False, message='要修改的用户不存在', error_code=const.code_param_illegal)
    if cur_user.user_type >= rel_change_user.user_type:
        return reply(success=False, message='无权限', error_code=const.code_not_permit)
    if rel_change_user.disabled == int(form.disabled.data):
        return reply(success=False, message='无需变更', error_code=const.code_param_illegal)
    update_data = dict()
    update_data['disabled'] = form.disabled.data
    res = utils.update_by_data(change_user, update_data, True)
    return reply(success=res[0], message=res[1], error_code=res[2])


def transform(user):
    item = pick(user,
                'id',
                'user_name',
                'user_alias',
                'user_number',
                'account_balance',
                'disabled',
                'dept_id'
                )
    dept = Department.query.filter_by(
        record_status=const.record_normal,
        id=user.dept_id,
    ).first()
    if user.user_type != const.user_type_admin:
        item['dept_name'] = dept.dept_name
    return item


@login_required_api
@ensure_session_removed
def query_user():
    current_page, page_size = utils.get_page_info(request)
    form = QueryUserForm(request.form)
    if not form.validate():
        return param_error(form.errors)
    user_query = dict()
    if form.id.data:
        user_query['id'] = form.id.data
    if form.user_name.data:
        user_query['user_name'] = form.user_name.data
    if form.user_alias.data:
        user_query['user_alias'] = form.user_alias.data
    if form.user_number.data:
        user_query['user_number'] = form.user_number.data
    if form.dept_id.data:
        user_query['dept_id'] = form.dept_id.data
    users = UserInfo.query.filter_by()
    if user_query:
        user_query['record_status'] = const.record_normal
        users = users.filter_by(
            **user_query
        )
    total_count = users.count()
    users = users.paginate(current_page, page_size, False).items
    data = map(lambda x: transform(x), users)
    data = list(data)
    return query_reply(success=True,
                       data=data,
                       paging={
                           'current': current_page,
                           'pages': int(total_count / page_size + 1),
                           'records': total_count,
                       },
                       message='done', error_code=const.code_success)
