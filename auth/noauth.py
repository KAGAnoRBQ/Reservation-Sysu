# coding: utf-8

from flask import Flask
from auth.interface import AuthInterface
from models import UserInfo, db, ensure_session_removed


class NoAuth(AuthInterface):
    def __init__(self, app: Flask, login_user):
        super().__init__(app, login_user)

    @ensure_session_removed
    def auth(self, *args, **kwargs):
        user = UserInfo.query.filter(UserInfo.id == 1).first()
        if not user:
            user = UserInfo()
            user.id = 1
            user.name = '匿名'
            user.username = 'anonymous'
            db.session.add(user)
            db.session.commit()
        self.login_user(user)
