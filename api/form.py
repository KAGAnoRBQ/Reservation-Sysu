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

class EditGymForm(wtforms.Form):
    id = wtforms.StringField(validators=[DataRequired()])
    gym_name = wtforms.StringField()
    location = wtforms.StringField()
    manager_number = wtforms.StringField()


class AddPeriodData(wtforms.Form):
    period_class_id = wtforms.StringField(validators=[DataRequired()])
    start_time = wtforms.DateTimeField(validators=[DataRequired()])
    end_time = wtforms.DateTimeField(validators=[DataRequired()])


class AddCourtResource(wtforms.Form):
    date = wtforms.DateTimeField(validators=[DataRequired()])
    period_id = wtforms.StringField(validators=[DataRequired()])
    court_id = wtforms.StringField(validators=[DataRequired()])
    court_number = wtforms.StringField(validators=[DataRequired()])
    occupied = wtforms.StringField(validators=[DataRequired()])
    max_order_count = wtforms.StringField(validators=[DataRequired()])
    order_count = wtforms.StringField(validators=[DataRequired()])


class AddShcedule(wtforms.Form):
    court_id = wtforms.StringField(validators=[DataRequired()])
    date = wtforms.DateTimeField(validators=[DataRequired()])
    total = wtforms.StringField(validators=[DataRequired()])
    order_count = wtforms.StringField(validators=[DataRequired()])
    occupied_count = wtforms.StringField(validators=[DataRequired()])
    visible = wtforms.StringField(validators=[DataRequired()])
    enabled = wtforms.StringField(validators=[DataRequired()])


class PayOrder(wtforms.Form):
    order_id = wtforms.StringField(validators=[DataRequired()])


class CancelOrder(wtforms.Form):
    cancel_order_id = wtforms.StringField(validators=[DataRequired()])


class SportFieldDefineForm(wtforms.Form):
    court_name = wtforms.StringField()
    court_description = wtforms.StringField()
    court_type = wtforms.IntegerField()
    court_number = wtforms.IntegerField()
    court_fee = wtforms.IntegerField()
    period_class_id = wtforms.IntegerField()


class EditSportFieldForm(wtforms.Form):
    id = wtforms.StringField(validators=[DataRequired()])
    court_name = wtforms.StringField()
    court_type = wtforms.StringField()
    court_num = wtforms.StringField()
    court_fee = wtforms.StringField()
    period_class_id = wtforms.StringField()
    order_days = wtforms.StringField()
    court_description = wtforms.StringField()


class AddSportFieldForm(wtforms.Form):
    gym_id = wtforms.StringField(DataRequired())
    court_name = wtforms.StringField(DataRequired())
    court_type = wtforms.StringField(DataRequired())
    court_num = wtforms.StringField(DataRequired())
    court_fee = wtforms.StringField(DataRequired())
    period_class_id = wtforms.StringField(DataRequired())
    order_days = wtforms.StringField(DataRequired())
    court_description = wtforms.StringField(DataRequired())


class PeriodClassForm(wtforms.Form):
    period_class_name = wtforms.StringField()
    period_description = wtforms.StringField()


class EditPeriodForm(wtforms.Form):
    period_id = wtforms.StringField()
    period_class_name = wtforms.StringField()
    period_description = wtforms.StringField()

class AddPeriodForm(wtforms.Form):
    period_class_name = wtforms.StringField(validators=[DataRequired()])
    period_description = wtforms.StringField(validators=[DataRequired()])
