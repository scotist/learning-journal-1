from pyramid.security import Allow, Everyone, ALL_PERMISSIONS


class DefaultRoot(object):

    __acl__ = [
        (Allow, 'norton', ['edit'])
    ]

    def __init__(self, request):
        self.request = request
