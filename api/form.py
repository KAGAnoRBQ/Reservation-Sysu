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


class EditGymForm(wtforms.Form):
    id = wtforms.StringField(validators=[DataRequired()])
    gym_name = wtforms.StringField()
    location = wtforms.StringField()
    manager_number = wtforms.StringField()
