# coding: utf-8
import wtforms

from wtforms.validators import *


class LoginForm(wtforms.Form):
    user_name = wtforms.StringField(validators=[DataRequired()])
    password = wtforms.StringField(validators=[DataRequired()])


class AddDepartmentForm(wtforms.Form):
    dept_name = wtforms.StringField(validators=[DataRequired()])


class RegisterForm(wtforms.Form):
    user_name = wtforms.StringField(validators=[DataRequired()])
    user_alias = wtforms.StringField(validators=[DataRequired()])
    user_number = wtforms.StringField(validators=[DataRequired()])
    dept_id = wtforms.StringField(validators=[DataRequired()])
    password = wtforms.StringField(validators=[DataRequired()])


class DeleteByIdForm(wtforms.Form):
    id = wtforms.StringField(validators=[DataRequired()])


class AddDeviceForm(wtforms.Form):
    code = wtforms.StringField(validators=[DataRequired()])
    name = wtforms.StringField(validators=[DataRequired()])
    model = wtforms.StringField(validators=[DataRequired()])
    brand = wtforms.StringField(validators=[DataRequired()])
    tag_code = wtforms.StringField(validators=[DataRequired()])
    description = wtforms.StringField(validators=[DataRequired()])
    manufacturer_date = wtforms.DateTimeField(validators=[DataRequired()])
    manufacturer_id = wtforms.StringField(validators=[DataRequired()])
    department_id = wtforms.StringField(validators=[DataRequired()])


class AddAchievementForm(wtforms.Form):
    device_code = wtforms.StringField(validators=[DataRequired()])
    member_code = wtforms.StringField(validators=[DataRequired()])
    manufacturer_date = wtforms.DateTimeField(validators=[DataRequired()])
    achievement_description = wtforms.StringField(validators=[DataRequired()])
    patent_description = wtforms.StringField(validators=[DataRequired()])
    paper_description = wtforms.StringField(validators=[DataRequired()])
    competition_description = wtforms.StringField(validators=[DataRequired()])
    achievement_remark = wtforms.StringField(validators=[DataRequired()])


class AddMemberForm(wtforms.Form):
    code = wtforms.StringField(validators=[DataRequired()])
    name = wtforms.StringField(validators=[DataRequired()])
    department_id = wtforms.StringField(validators=[DataRequired()])


class AddManufacturerForm(wtforms.Form):
    name = wtforms.StringField(validators=[DataRequired()])


class RentDeviceForm(wtforms.Form):
    device_code = wtforms.StringField(validators=[DataRequired()])
    borrower_member_code = wtforms.StringField(validators=[DataRequired()])
    borrow_date = wtforms.DateTimeField(validators=[DataRequired()])
    borrow_remark = wtforms.StringField(validators=[DataRequired()])
    expect_return_date = wtforms.DateTimeField(validators=[DataRequired()])


class ReturnDeviceForm(wtforms.Form):
    device_code = wtforms.StringField(validators=[DataRequired()])
    returner_member_code = wtforms.StringField(validators=[DataRequired()])
    return_date = wtforms.DateTimeField(validators=[DataRequired()])
    return_remark = wtforms.StringField(validators=[DataRequired()])


class QueryMemberForm(wtforms.Form):
    id = wtforms.StringField()
    code = wtforms.StringField()
    name = wtforms.StringField()


class QueryDefaultForm(wtforms.Form):
    page = wtforms.IntegerField()
    limit = wtforms.IntegerField()

class AddPeriodData(wtforms.Form):
    period_id = wtforms.IntegerField()
    period_class_id = wtforms.IntegerField()
    start_time = wtforms.DateTimeField(validators=[DataRequired()])
    end_time = wtforms.DateTimeField(validators=[DataRequired()])

class AddCourtResource(wtforms.Form):
    source_id = wtforms.IntegerField()
    date = wtforms.DateTimeField(validators=[DataRequired()])
    period_id = wtforms.IntegerField()
    court_id = wtforms.IntegerField()
    court_number = wtforms.IntegerField()
    occupied = wtforms.BooleanField()
    max_order_court = wtforms.IntegerField()
    order_count = wtforms.IntegerField()

class AddShcedule(wtforms.Form):
    resource_id = wtforms.IntegerField()
    court_id = wtforms.IntegerField()
    date = wtforms.DateTimeField(validators=[DataRequired()])
    total = wtforms.IntegerField()
    order_count = wtforms.IntegerField()
    occupied_count = wtforms.IntegerField()
    visible = wtforms.BooleanField()
    enabled = wtforms.BooleanField()

