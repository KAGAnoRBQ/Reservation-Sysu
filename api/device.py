from common.views import login_required_api
from api.form import AddDeviceForm, DeleteByIdForm
from flask import request
from common import const, utils
from common.response import reply
from models import Device, Manufacturer, Department, ensure_session_removed


@login_required_api
@ensure_session_removed
def add_device():
    form = AddDeviceForm(request.form)
    if not form.validate():
        return reply(success=False, message='参数错误', error_code=const.param_err)

    if utils.is_code_exist(Device, form.code.data)[0]:
        return reply(success=False, message='该设备编码已存在', error_code=const.param_illegal)

    if not utils.is_id_exist(Department, form.department_id.data)[0]:
        return reply(success=False, message='该部门不存在', error_code=const.param_illegal)

    if not utils.is_id_exist(Manufacturer, form.manufacturer_id.data)[0]:
        return reply(success=False, message='该生产厂家不存在', error_code=const.param_illegal)

    device_data = {
        'code': form.code.data,
        'name': form.name.data,
        'model': form.model.data,
        'brand': form.brand.data,
        'tag_code': form.tag_code.data,
        'description': form.description.data,
        'status': const.Returned,
        'manufacturer_date': form.manufacturer_date.data,
        'manufacturer_id': form.manufacturer_id.data,
        'department_id': form.department_id.data,
        'record_status': const.Normal,
    }
    res = utils.add_by_data(Device, device_data)
    return reply(success=res[0], message=res[1], error_code=res[2])


@login_required_api
@ensure_session_removed
def delete_device():
    form = DeleteByIdForm(request.form)
    if not form.validate():
        return reply(success=False, message='参数错误', error_code=const.param_err)

    res = utils.delete_by_id(Device, form.id.data)
    return reply(success=res[0], message=res[1], error_code=res[2])
