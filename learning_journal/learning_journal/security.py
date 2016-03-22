import os
from passlib.apps import custom_app_context as pwd_context


def check_pw(pw):
    hashed = os.environ.get('AUTH_PASSWORD', 'this is not a password')
    return pwd_context.verify(pw, hashed)


def groupfinder(userid, request):
    if userid in USERS:
        return USERS.get(userid, [])


# class DefaultRoot(object:
#                   __acl__=[
#                            (Allow, Everyone, 'view'),
#                            (Allow, 'g:users', 'read'),
#                            (Allow, 'g:users', 'create'),
#                            (Allow, 'g:admins', 'ALL_PERMISSIONS'),
#                           ])

#     def __init__(self, request):
#         self.request = request

#     def groupfinder(userid, request):
#         groups = []
#         if userid.lower() in request.approved:
#             groups.append('g:users')
#         if userid.lower() in request.admins:
#             groups.append('g:admins')
#         return groups or None


# class EntryRoot(object):

#     __name__ = 'entry'

#     @property
#     def __parent__(self):
#         return DefaultRoot(self.request)

#     def __init__(self, request):
#         self.request = request

#     def __getitem__()
