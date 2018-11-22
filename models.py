# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import (
    BIGINT, VARCHAR, DATETIME, BOOLEAN, TINYINT, TEXT, DATE, TIME
)
from flask_login import UserMixin
import functools
from datetime import datetime
from common import const

db = SQLAlchemy()


def ensure_session_removed(func):
    @functools.wraps(func)
    def _func(*args, **kws):
        try:
            return func(*args, **kws)
        finally:
            db.session.remove()

    return _func


def db_commit():
    try:
        db.session.commit()
        return True, '', const.code_success
    except:
        return False, '数据库操作失败', const.code_db_err


class MySQLMixin(object):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }


class UserInfo(db.Model, MySQLMixin, UserMixin):
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    user_name = db.Column(VARCHAR(255), nullable=False)
    user_alias = db.Column(VARCHAR(255), nullable=False)
    user_number = db.Column(VARCHAR(255), nullable=False)
    user_type = db.Column(TINYINT(unsigned=True), default=0)
    dept_id = db.Column(BIGINT(unsigned=True), nullable=False)
    password = db.Column(VARCHAR(255), nullable=False)
    account_balance = db.Column(BIGINT(unsigned=True), nullable=False)
    disabled = db.Column(TINYINT(unsigned=True), default=0)
    record_status = db.Column(TINYINT(unsigned=True), default=0)  # 0---code_success 1---delete
    create_time = db.Column(DATETIME, default=datetime.now)
    update_time = db.Column(DATETIME, default=datetime.now)

    def to_json(self):
        _dict = self.__dict__
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        return _dict


class Gym(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    gym_name = db.Column(VARCHAR(255), nullable=False)
    location = db.Column(VARCHAR(255), nullable=False)
    manager_id = db.Column(BIGINT(unsigned=True), nullable=False)
    record_status = db.Column(TINYINT(unsigned=True), default=0)
    create_time = db.Column(DATETIME, default=datetime.now)
    update_time = db.Column(DATETIME, default=datetime.now)

    def to_json(self):
        _dict = self.__dict__
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        return _dict


class Department(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    dept_name = db.Column(VARCHAR(255), nullable=False)
    record_status = db.Column(TINYINT(unsigned=True), default=0)
    create_time = db.Column(DATETIME, default=datetime.now)
    update_time = db.Column(DATETIME, default=datetime.now)

    def to_json(self):
        _dict = self.__dict__
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]


class Device(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    code = db.Column(VARCHAR(255), nullable=False)
    name = db.Column(VARCHAR(255), nullable=False)
    model = db.Column(VARCHAR(255), nullable=False)
    brand = db.Column(VARCHAR(255), nullable=False)
    tag_code = db.Column(VARCHAR(255), nullable=False)
    status = db.Column(TINYINT(unsigned=True), default=0)
    manufacturer_id = db.Column(VARCHAR(255), nullable=False)
    manufacturer_date = db.Column(DATETIME, default='')
    department_id = db.Column(BIGINT(unsigned=True), nullable=False)
    record_status = db.Column(TINYINT(unsigned=True), default=0)
    create_time = db.Column(DATETIME, default=datetime.now)
    update_time = db.Column(DATETIME, default=datetime.now)
    description = db.Column(VARCHAR(1020), nullable=False)


class Manufacturer(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    name = db.Column(VARCHAR(255), nullable=False)
    record_status = db.Column(TINYINT(unsigned=True), default=0)  # 0---code_success 1---delete
    create_time = db.Column(DATETIME, default=datetime.now)
    update_time = db.Column(DATETIME, default=datetime.now)


class Member(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    code = db.Column(VARCHAR(255), nullable=False)
    name = db.Column(VARCHAR(255), nullable=False)
    department_id = db.Column(BIGINT(unsigned=True), nullable=False)
    record_status = db.Column(TINYINT(unsigned=True), default=0)
    create_time = db.Column(DATETIME, default=datetime.now)
    update_time = db.Column(DATETIME, default=datetime.now)


class DeviceRent(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    device_code = db.Column(VARCHAR(255), nullable=False)
    status = db.Column(TINYINT(unsigned=True), default=0)
    borrower_member_code = db.Column(VARCHAR(255), nullable=False)
    borrow_date = db.Column(DATETIME, default=datetime.now)
    expect_return_date = db.Column(DATETIME, default=datetime.now)
    borrow_remark = db.Column(VARCHAR(1020), nullable=False)
    returner_member_code = db.Column(VARCHAR(255), nullable=False)
    real_return_date = db.Column(DATETIME, default=datetime.now)
    return_remark = db.Column(VARCHAR(1020), nullable=False)
    record_status = db.Column(TINYINT(unsigned=True), default=0)
    create_time = db.Column(DATETIME, default=datetime.now)
    update_time = db.Column(DATETIME, default=datetime.now)


class Achievement(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    device_code = db.Column(BIGINT(unsigned=True), nullable=False)
    member_code = db.Column(BIGINT(unsigned=True), nullable=False)
    manufacturer_date = db.Column(DATETIME, default=datetime.now)
    achievement_description = db.Column(VARCHAR(1020), nullable=False)
    patent_description = db.Column(VARCHAR(1020), nullable=False)
    paper_description = db.Column(VARCHAR(1020), nullable=False)
    competition_description = db.Column(VARCHAR(1020), nullable=False)
    achievement_remark = db.Column(VARCHAR(1020), nullable=False)
    record_status = db.Column(TINYINT(unsigned=True), default=0)
    create_time = db.Column(DATETIME, default=datetime.now)
    update_time = db.Column(DATETIME, default=datetime.now)


# period_class: 时间段类型，里面是可用时间段的名称和描述
class PeriodClass(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    period_class_name = db.Column(VARCHAR(64), nullable=False)
    period_class_description = db.Column(VARCHAR(240), nullable=False)


# 时间段数据，作为上面的时间段类型的具体数据的描述，比如时间段的起始时间、结束时间等
class PeriodData(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    period_class_id = db.Column(BIGINT(unsigned=True), nullable=False)
    start_time = db.Column(TIME, nullable=False)
    end_time = db.Column(TIME, nullable=False)


# Court类用来表示场地
class Court(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    gym_id = db.Column(BIGINT(unsigned=True), nullable=False)
    court_name = db.Column(VARCHAR(32),nullable=False)
    description = db.Column(TEXT, nullable=True)
    court_type = db.Column(BIGINT(unsigned=True), nullable=False)
    court_count = db.Column(BIGINT(unsigned=True), nullable=False)
    max_order_count = db.Column(BIGINT(unsigned=True), nullable=False)
    court_fee = db.Column(BIGINT(unsigned=True), nullable=False)
    order_days = db.Column(BIGINT(unsigned=True), nullable=False)
    period_class_id = db.Column(BIGINT(unsigned=True), nullable=False)


# court_resource 场地资源
class CourtResource(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    date = db.Column(DATE, nullable=False)
    period_id = db.Column(BIGINT(unsigned=True), nullable=False)
    court_id = db.Column(BIGINT(unsigned=True),  nullable=False)
    court_number = db.Column(BIGINT(unsigned=True), nullable=False)
    occupied = db.Column(TINYINT(unsigned=True), nullable=False)
    max_order_count = db.Column(BIGINT(unsigned=True), nullable=False)
    order_count = db.Column(BIGINT(unsigned=True), nullable=False)


# schedule: 用于描述某种场地，比如羽毛球场地，在某天被订场的数量，占场的数量
class Schedule(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    court_id = db.Column(BIGINT(unsigned=True), nullable=False)
    date = db.Column(DATE, nullable=False)
    total = db.Column(BIGINT(unsigned=True), nullable=False)
    ordered_count = db.Column(BIGINT(unsigned=True), nullable=False)
    occupied_count = db.Column(BIGINT(unsigned=True), nullable=False)
    visible = db.Column(TINYINT(unsigned=True), default=0)
    enabled = db.Column(TINYINT(unsigned=True), default=1)


class CourtOrder(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    user_id = db.Column(BIGINT(unsigned=True), nullable=False)
    order_time = db.Column(DATETIME, default=datetime.now())
    resource_id = db.Column(BIGINT(unsigned=True), nullable=False)
    pay_time = db.Column(DATETIME, default=datetime.now())
    amount = db.Column(BIGINT(unsigned=True), nullable=False)
    is_ackd = db.Column(TINYINT(unsigned=True), default=0)
    ack_time = db.Column(DATETIME, default=datetime.now())
    is_canceled = db.Column(TINYINT(unsigned=True), default=0)
    # is_paid = db.Column(TINYINT(unsigned=True), default=0)  # 新增字段表示当前表单是否已经付款
    cancel_time = db.Column(DATETIME, default=datetime.now())
    is_used = db.Column(TINYINT(unsigned=True), default=0)
    # record_status = db.Column(TINYINT(unsigned=True), default=0)
    # create_time = db.Column(DATETIME, default=datetime.now)
    # update_time = db.Column(DATETIME, default=datetime.now)


# account: 财务账户
class Account(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    user_id = db.Column(BIGINT(unsigned=True), nullable=False)
    order_id = db.Column(BIGINT(unsigned=True), nullable=False)
    account_summary = db.Column(VARCHAR(64), nullable=True)
    account_time = db.Column(DATETIME, nullable=False)
    amount = db.Column(BIGINT, nullable=False)


# option
class Option(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    pre_days = db.Column(BIGINT(unsigned=True), nullable=False)
    admin_pass = db.Column(VARCHAR(32), nullable=False)
