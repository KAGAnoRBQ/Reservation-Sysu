from common.views import login_required_api
from api.form import RentDeviceForm, DeleteByIdForm, ReturnDeviceForm
from flask import request
from common import const, utils
from common.response import reply
from models import DeviceRent, Device, Member, ensure_session_removed


@login_required_api
@ensure_session_removed
def rent_device():
    form = RentDeviceForm(request.form)
    if not form.validate():
        return reply(success=False, message='参数错误', error_code=const.param_err)
    res_device = utils.is_code_exist(Device, form.device_code.data)
    if not res_device[0]:
        return reply(success=False, message='该设备不存在', error_code=const.param_illegal)
    device = res_device[1].first()
    if device.status != const.Returned:
        return reply(success=False, message='该设备已被借出', error_code=const.param_illegal)

    if not utils.is_code_exist(Member, form.borrower_member_code.data)[0]:
        return reply(success=False, message='该成员不存在', error_code=const.param_illegal)

    update_info = {
        'status': const.Rented,
    }
    if not utils.update_by_data(res_device[1], update_info, False)[0]:
        return reply(success=False, message='设备状态修改失败', error_code=const.unknown_err)

    device_rent_data = {
        'device_code': form.device_code.data,
        'status': const.Rented,
        'borrower_member_code': form.borrower_member_code.data,
        'borrow_date': form.borrow_date.data,
        'borrow_remark': form.borrow_remark.data,
        'expect_return_date': form.expect_return_date.data,
        # default
        'returner_member_code': '',
        'real_return_date': form.expect_return_date.data,
        'return_remark': '',
        'record_status': const.Normal,
    }
    res = utils.add_by_data(DeviceRent, device_rent_data)

    return reply(success=res[0], message=res[1], error_code=res[2])


@login_required_api
@ensure_session_removed
def return_device():
    form = ReturnDeviceForm(request.form)
    if not form.validate():
        return reply(success=False, message='参数错误', error_code=const.param_err)

    res_device = utils.is_code_exist(Device, form.device_code.data)
    if not res_device[0]:
        return reply(success=False, message='该设备不存在', error_code=const.param_illegal)
    device = res_device[1].first()
    if device.status != const.Rented:
        return reply(success=False, message='该设备未被借出', error_code=const.param_illegal)

    device_rented = DeviceRent.query.filter_by(
        device_code=form.device_code.data,
        status=const.Rented,
        record_status=const.Normal
    )
    cnt = device_rented.count()
    if cnt < 1:
        return reply(success=False, message='无此设备正在外借记录', error_code=const.unknown_err)
    if cnt > 1:
        return reply(success=False, message='内部数据错误，请联系管理员', error_code=const.unknown_err)

    if not utils.is_code_exist(Member, form.returner_member_code.data)[0]:
        return reply(success=False, message='该归还成员不存在', error_code=const.param_illegal)

    update_info = {
        'status': const.Returned,
    }
    if not utils.update_by_data(res_device[1], update_info, False)[0]:
        return reply(success=False, message='设备状态修改失败', error_code=const.unknown_err)

    device_return_data = {
        'status': const.Returned,
        'returner_member_code': form.returner_member_code.data,
        'real_return_date': form.return_date.data,
        'return_remark': form.return_remark.data,
    }
    res = utils.update_by_data(device_rented, device_return_data, True)

    return reply(success=res[0], message=res[1], error_code=res[2])
    # return reply(success=True)


@login_required_api
@ensure_session_removed
def delete_device_rent():
    form = DeleteByIdForm(request.form)
    if not form.validate():
        return reply(success=False, message='参数错误', error_code=const.param_err)
    res = utils.delete_by_id(DeviceRent, form.id.data)
    return reply(success=res[0], message=res[1], error_code=res[2])
