# coding: utf-8
from models import db, UserInfo
from common.views import login_required


# @login_required
def db_add():
    user_data = {
        'id': 10,
        'user_name': 'test_name',
        'password': 'test'
    }
    user_info = UserInfo(**user_data)
    db.session.add(user_info)
    db.session.commit()
    return dict(
        success='code_success'
    )
