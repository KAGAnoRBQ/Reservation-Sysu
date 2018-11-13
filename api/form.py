# coding: utf-8
import wtforms

from wtforms.validators import *


class LoginForm(wtforms.Form):
    user_number = wtforms.StringField(validators=[DataRequired()])
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


class ChangePermissionForm(wtforms.Form):
    user_id = wtforms.StringField(validators=[DataRequired()])
    user_type = wtforms.StringField(validators=[DataRequired()])


class ChangeDisableForm(wtforms.Form):
    user_id = wtforms.StringField(validators=[DataRequired()])
    disabled = wtforms.StringField(validators=[DataRequired()])


class QueryUserForm(wtforms.Form):
    id = wtforms.StringField()
    user_name = wtforms.StringField()
    user_alias = wtforms.StringField()
    user_number = wtforms.StringField()
    dept_id = wtforms.StringField()


class AddGymForm(wtforms.Form):
    gym_name = wtforms.StringField(validators=[DataRequired()])
    location = wtforms.StringField(validators=[DataRequired()])
    manager_number = wtforms.StringField(validators=[DataRequired()])


class QueryGymForm(wtforms.Form):
    gym_name = wtforms.StringField()
    location = wtforms.StringField()
    manager_number = wtforms.StringField()


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

class EditGymForm(wtforms.Form):
    id = wtforms.StringField(validators=[DataRequired()])
    gym_name = wtforms.StringField()
    location = wtforms.StringField()
    manager_number = wtforms.StringField()
