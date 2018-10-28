from common.views import login_required_api
from api.form import AddDepartmentForm, DeleteByIdForm
from flask import request
from common import const, utils
from common.response import reply
from models import Department, ensure_session_removed
from pydash import pick


@login_required_api
@ensure_session_removed
def add_department():
    form = AddDepartmentForm(request.form)
    if not form.validate():
        return reply(success=False, message='参数错误', error_code=const.code_param_err)

    department_data = {
        'dept_name': form.dept_name.data,
        'record_status': const.record_normal,
    }
    res = utils.add_by_data(Department, department_data)
    return reply(success=res[0], message=res[1], error_code=res[2])


@login_required_api
@ensure_session_removed
def delete_department():
    form = DeleteByIdForm(request.form)
    if not form.validate():
        return reply(success=False, message='参数错误', error_code=const.code_param_err)

    res = utils.delete_by_id(Department, form.id.data)
    return reply(success=res[0], message=res[1], error_code=res[2])


@login_required_api
def query_department():
    departments = Department.query.order_by(
        Department.dept_name
    ).filter_by(
        record_status=const.record_normal
    ).all()
    data = []
    for department in departments:
        data.append(department.to_json())
    return reply(success=True, data=data, message='done', error_code=const.code_success)
