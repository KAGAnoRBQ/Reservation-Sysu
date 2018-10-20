from common.views import login_required_api
from api.form import AddMemberForm, DeleteByIdForm, QueryMemberForm
from flask import request
from common import const, utils
from common.response import reply
from models import Member, Department, ensure_session_removed
from pydash import pick


@login_required_api
@ensure_session_removed
def add_member():
    form = AddMemberForm(request.form)
    if not form.validate():
        return reply(success=False, message='参数错误', error_code=const.param_err)

    if utils.is_code_exist(Member, form.code.data)[0]:
        return reply(success=False, message='该成员编码已存在', error_code=const.param_illegal)

    if not utils.is_id_exist(Department, form.department_id.data)[0]:
        return reply(success=False, message='该部门不存在', error_code=const.param_illegal)

    member_data = {
        'code': form.code.data,
        'name': form.name.data,
        'department_id': form.department_id.data,
        'record_status': const.Normal,
    }
    res = utils.add_by_data(Member, member_data)
    return reply(success=res[0], message=res[1], error_code=res[2])


fileds = ['id', 'code', 'name']


def tran_to_json(record):
    item = pick(record, fileds)
    return item


@login_required_api
def query_member():
    page_info = utils.get_page_info(request)
    current_page = page_info[0]
    page_size = page_info[1]
    form = QueryMemberForm(request.form)
    if not form.validate():
        return reply(success=False, message='参数错误', error_code=const.param_err)
    members = Member.query.filter_by()
    query_dict = dict()
    if form.id.data:
        query_dict['id'] = form.id.data
    if form.code.data:
        query_dict['code'] = form.id.data
    if form.name.data:
        query_dict['name'] = form.id.data
    if query_dict:
        members = members.filter_by(**query_dict)
    members = Member.query.filter_by(
        record_status=const.Normal
    )

    total_count = members.count()
    members = members.paginate(current_page, page_size, False).items
    data = map(lambda x: tran_to_json(x), members)
    data = list(data)
    return reply(success=True,
                 data={
                     'items': data,
                     'total_count': total_count,
                 },
                 message='done', error_code=const.success)


@login_required_api
@ensure_session_removed
def delete_member():
    form = DeleteByIdForm(request.form)
    if not form.validate():
        return reply(success=False, message='参数错误', error_code=const.param_err)

    res = utils.delete_by_id(Member, form.id.data)
    return reply(success=res[0], message=res[1], error_code=res[2])
