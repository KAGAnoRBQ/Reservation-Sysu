import wtforms

from wtforms.validators import *


class LoginForm(wtforms.Form):
    username = wtforms.StringField(validators=[DataRequired()])
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


class AddDepartmentForm(wtforms.Form):
    code = wtforms.StringField(validators=[DataRequired()])
    name = wtforms.StringField(validators=[DataRequired()])


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
