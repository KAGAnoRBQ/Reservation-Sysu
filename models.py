from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import (
    BIGINT, VARCHAR, DATETIME, BOOLEAN, TINYINT, INTEGER
)
from flask_login import UserMixin
import functools
from datetime import datetime
from common import const
import logging

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
        return True, '操作成功', const.code_success
    except Exception as exc:
        logging.warning(exc)
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
        return _dict


class Account(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    user_id = db.Column(BIGINT(unsigned=True), default=0)
    order_id = db.Column(BIGINT(unsigned=True), default=0)
    account_summary = db.Column(VARCHAR(length=64), default="")
    account_time = db.Column(DATETIME, default=datetime.now())
    amount = db.Column(INTEGER, default=0)

    def to_json(self):
        _dict = self.__dict__
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        return _dict


class Gym(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    gym_name = db.Column(VARCHAR(255), nullable=False)
    location = db.Column(VARCHAR(255), nullable=False)
    manager_number = db.Column(BIGINT(unsigned=True), nullable=False)
    record_status = db.Column(TINYINT(unsigned=True), default=0)
    create_time = db.Column(DATETIME, default=datetime.now)
    update_time = db.Column(DATETIME, default=datetime.now)

    def to_json(self):
        _dict = self.__dict__
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        return _dict


class Court(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    gym_id = db.Column(BIGINT(unsigned=True), default=0)
    court_name = db.Column(VARCHAR(length=32), default="")
    description = db.Column(db.TEXT, default="")
    court_type = db.Column(TINYINT, default=0)
    court_count = db.Column(INTEGER(unsigned=True), default=0)
    max_order_count = db.Column(INTEGER(unsigned=True), default=1)
    court_fee = db.Column(INTEGER(unsigned=True), default=0)
    order_days = db.Column(INTEGER(unsigned=True), default=1)
    period_class_id = db.Column(INTEGER(unsigned=True), default=0)

    def to_json(self):
        _dict = self.__dict__
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        return _dict


class PeriodClass(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    period_class_name = db.Column(VARCHAR(64), default="")
    period_class_description = db.Column(VARCHAR(240), default="")

    def to_json(self):
        _dict = self.__dict__
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        return _dict


class PeriodData(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    period_class_id = db.Column(BIGINT(unsigned=True), default=0)
    start_time = db.Column(DATETIME, default=datetime.now())
    end_time = db.Column(DATETIME, default=datetime.now())

    def to_json(self):
        _dict = self.__dict__
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        return _dict


class Schedule(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    court_id = db.Column(BIGINT(unsigned=True), default=0)
    date = db.Column(DATETIME, default=datetime.now())
    total = db.Column(INTEGER(unsigned=True), default=0)
    ordered_count = db.Column(INTEGER(unsigned=True), default=0)
    occupied_count = db.Column(INTEGER(unsigned=True), default=0)
    visible = db.Column(BOOLEAN, default=False)
    enabled = db.Column(BOOLEAN, default=True)

    def to_json(self):
        _dict = self.__dict__
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        return _dict


class CourtResource(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    date = db.Column(DATETIME, default=datetime.now())
    period_id = db.Column(BIGINT(unsigned=True), default=0)
    court_id = db.Column(BIGINT(unsigned=True), default=0)
    court_number = db.Column(BIGINT(unsigned=True), default=0)
    occupied = db.Column(BOOLEAN, default=False)
    max_order_count = db.Column(INTEGER, default=0)

    def to_json(self):
        _dict = self.__dict__
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        return _dict


class CourtOrder(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    user_id = db.Column(BIGINT(unsigned=True), default=0)
    order_time = db.Column(DATETIME, default=datetime.now())
    resource_id = db.Column(BIGINT(unsigned=True), default=0)
    pay_time = db.Column(DATETIME, default=datetime.now())
    amount = db.Column(INTEGER(unsigned=True), default=0)
    is_ackd = db.Column(BOOLEAN, default=False)
    ack_time = db.Column(DATETIME, default=datetime.now())
    is_canceled = db.Column(BOOLEAN, default=False)
    cancel_time = db.Column(BOOLEAN, default=datetime.now())
    is_used = db.Column(BOOLEAN, default=False)

    def to_json(self):
        _dict = self.__dict__
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        return _dict


class Option(db.Model, MySQLMixin):
    id = db.Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    pre_days = db.Column(INTEGER(unsigned=True), default=0)
    admin_pass = db.Column(VARCHAR(32))

    def to_json(self):
        _dict = self.__dict__
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        return _dict


#############################################################
#                        分割线                             #
#############################################################

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
