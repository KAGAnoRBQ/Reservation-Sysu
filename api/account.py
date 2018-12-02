# -*- coding: utf-8 -*-

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


def get_user_account(account):
    item = {
        'account_time': account.account_time,
        'order_id': account.order_id,
        'account_summary': account.account_summary,
        'amount': account.amount,
        'account_balance': 0
    }

    return item


def get_manager_account(account):
    user = UserInfo.query.filter(UserInfo.id == account.user_id).first()
    item = {
        'user_name': user.user_name,
        'user_number': user.user_number,
        'account_time': account.account_time,
        'order_id': account.order_id,
        'account_summary': account.account_summary,
        'amount': account.amount,
        'account_balance': 0
    }

    return item


@login_required_api
def account_user_query():
    current_page, page_size = utils.get_page_info(request)
    accounts = Account.query.filter(Account.user_id == current_user.id)
    total_count = accounts.count()
    accounts = accounts.paginate(current_page, page_size, False).items
    accounts = map(lambda account: get_user_account(account), accounts)
    accounts = list(accounts)
    return query_reply(success=True,
                       data={'accounts': accounts},
                       paging={
                           'current': current_page,
                           'pages': int((total_count - 1) / page_size + 1),
                           'records': total_count,
                       },
                       message='done', error_code=const.code_success)


@login_required_api
def account_manager_query():
    if current_user.user_type != const.user_type_manage:
        return reply(success=False, message='无权限', error_code=const.code_not_permit)

    current_page, page_size = utils.get_page_info(request)
    accounts = Account.query.order_by(Account.account_time)
    total_count = accounts.count()
    accounts = accounts.paginate(current_page, page_size, False).items
    accounts = map(lambda account: get_manager_account(account), accounts)
    accounts = list(accounts)
    return query_reply(success=True,
                       data={'accounts': accounts},
                       paging={
                           'current': current_page,
                           'pages': int((total_count - 1) / page_size + 1),
                           'records': total_count,
                       },
                       message='done', error_code=const.code_success)


@login_required_api
@ensure_session_removed
def account_deposit():
    user_ids = request.json.get('user_ids')
    amount = (int)(request.json.get('amount'))
    users = UserInfo.query.filter(UserInfo.id.in_(user_ids), UserInfo.record_status == const.record_normal).all()

    for user in users:
        user.update_time = datetime.now()
        user.account_balance += amount
        account = Account(user_id=user.id, order_id=0, account_summary='充值', account_time=datetime.now(), amount=amount)
        db.session.add(account)

    res = db_commit()
    return reply(success=res[0], message=res[1], error_code=res[2])


@login_required_api
def account_clear_balance():
    user_ids = request.json.get('user_ids')
    users = UserInfo.query.filter(UserInfo.id.in_(user_ids), UserInfo.record_status == const.record_normal).all()
    for user in users:
        user.update_time = datetime.now()
        account = Account(user_id=user.id, order_id=0, account_summary='清零', account_time=datetime.now(), amount=user.account_balance)
        user.account_balance = 0
        db.session.add(account)
    res = db_commit()
    return reply(success=res[0], message=res[1], error_code=res[2])


@login_required_api
def account_query_balance():
    user_id = request.args.get('user_id', current_user.id)

    if user_id != current_user and current_user.user_type != const.user_type_manage:
        return reply(success=False, message='无权限', error_code=const.code_not_permit)

    if user_id != current_user:
        user = UserInfo.query.filter(UserInfo.id == user_id, UserInfo.record_status == const.record_normal).first()
        if not user:
            return reply(success=False, message='非法用户id', error_code=const.code_param_illegal)
        balance = user.account_balance
    else:
        balance = current_user.account_balance

    return reply(success=True,
                 data={'user_balance': balance},
                 message='done', error_code=const.code_success)
