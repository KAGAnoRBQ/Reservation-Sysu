# coding: utf-8

import json
from common import const
from datetime import datetime
from models import db, db_commit
import logging


def param_error(errors):
    return {
        'code_success': False,
        'message': '参数错误:%s。' % json.dumps(errors)
    }


def add_by_data(table, data, do_commit=True):
    record = table(**data)
    db.session.add(record)
    resp = [True, '', const.code_success]
    if do_commit:
        resp = db_commit()
    return resp


def update_by_data(records, update_data, do_commit=True):
    update_data['update_time'] = datetime.now()
    records.update(update_data)
    resp = [True, '', const.code_success]
    if do_commit:
        resp = db_commit()
    return resp


delete_info = {
    'record_status': const.record_deleted,
    'update_time': datetime.now()
}


def delete_by_id(table, id, do_commit=True):
    res = is_id_exist(table, id)
    if res[0]:
        delete_info['update_time'] = datetime.now()
        res[1].update(delete_info)
        resp = [True, '', const.code_success]
        if do_commit:
            resp = db_commit()
        return resp
    return False, '记录不存在', const.code_param_illegal


def is_code_exist(table, data):
    ext = table.query.filter_by(
        code=data,
        record_status=const.record_normal
    )
    if not ext.first():
        return False, None
    return True, ext


def is_id_exist(table, data):
    ext = table.query.filter_by(
        id=data,
        record_status=const.record_normal
    )
    if not ext.first():
        return False, None
    return True, ext


def is_name_exist(table, data):
    ext = table.query.filter_by(
        name=data,
        record_status=const.record_normal
    )
    if not ext.first():
        return False, None
    return True, ext


def get_page_info(request):
    current_page = request.args.get('page')
    if not current_page:
        current_page = const.current_page_default
    page_size = request.args.get('limit')
    if not page_size:
        page_size = const.page_size_default
    return int(current_page), int(page_size)


def get_gym_id(request):
    current_gym = request.args.get('gym_id')
    if not current_gym:
        current_gym = const.current_gym_default
    return int(current_gym)


def get_sportsfield_id(request):
    current_sportsfield = request.args.get('court_id')
    if not current_sportsfield:
        current_sportsfield = const.current_court_default
    return int(current_sportsfield)

def get_period_class_id(request):
    current_period_id = request.args.get('period_id')
    if not current_period_id:
        current_period_id = const.current_period_class_default
    return int(current_period_id)

def get_real_period_class_id(request):
    period_class_id = request.args.get('period_class_id')
    if not period_class_id:
        period_class_id = const.current_period_class_default
    return int(period_class_id)

def get_period_id(request):
    period_id = request.args.get('period_id', None)
    if period_id is None:
        return period_id
    return int(period_id)

def get_court_resource_id(request):
    court_resource_id = request.args.get('court_resource_id', None)
    if court_resource_id is None:
        return court_resource_id
    return int(court_resource_id)

def get_court_id(request):
    court_id = request.args.get('court_id')
    if not court_id:
        court_id = const.court_id_default
    return int(court_id)

def get_schedule_id(request):
    schedule_id = request.args.get('schedule_id')
    if schedule_id is None:
        return schedule_id
    return int(schedule_id)

