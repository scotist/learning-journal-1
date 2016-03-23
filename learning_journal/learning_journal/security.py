import os
from passlib.apps import custom_app_context as pwd_context
from pyramid.security import Allow, Everyone, ALL_PERMISSIONS


def check_pw(pw):
    hashed = os.environ.get('AUTH_PASSWORD', 'this is not a password')
    return pwd_context.verify(pw, hashed)


def groupfinder(userid, request):
    if userid in USERS:
        return USERS.get(userid, [])


class DefaultRoot(object):

    __acl__ = [
        (Allow, 'scotist', ['edit', 'create'])
    ]

    def __init__(self, request):
        self.request = request
