from pyramid.security import Allow, Everyone, ALL_PERMISSIONS


class DefaultRoot(object):

    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, 'norton', ['edit', 'view'])
    ]

    def __init__(self, request):
        self.request = request
