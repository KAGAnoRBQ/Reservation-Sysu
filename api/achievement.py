from common.views import login_required_api
from api.form import AddAchievementForm, DeleteByIdForm
from flask import request
from common import const, utils
from common.response import reply
from models import Device, Achievement, Member, ensure_session_removed


@login_required_api
@ensure_session_removed
def add_achievement():
    form = AddAchievementForm(request.form)
    if not form.validate():
        return reply(success=False, message='参数错误', error_code=const.param_err)

    if not utils.is_code_exist(Device, form.device_code.data)[0]:
        return reply(success=False, message='设备不存在', error_code=const.param_illegal)
    if not utils.is_code_exist(Member, form.member_code.data)[0]:
        return reply(success=False, message='成员不存在', error_code=const.param_illegal)

    device_achievement_data = {
        'device_code': form.device_code.data,
        'member_code': form.member_code.data,
        'manufacturer_date': form.manufacturer_date.data,
        'achievement_description': form.achievement_description.data,
        'patent_description': form.patent_description.data,
        'paper_description': form.paper_description.data,
        'competition_description': form.competition_description.data,
        'achievement_remark': form.achievement_remark.data,
        'record_status': const.Normal,
    }
    res = utils.add_by_data(Achievement, device_achievement_data)
    return reply(success=res[0], message=res[1], error_code=res[2])


@login_required_api
@ensure_session_removed
def delete_achievement():
    form = DeleteByIdForm(request.form)
    if not form.validate():
        return reply(success=False, message='参数错误', error_code=const.param_err)

    res = utils.delete_by_id(Achievement, form.id.data)
    return reply(success=res[0], message=res[1], error_code=res[2])
