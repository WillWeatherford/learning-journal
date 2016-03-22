"""Set up security standards for the journal app."""
# from .models import Entry
from pyramid.security import Allow, Everyone, ALL_PERMISSIONS
from cryptacular.bcrypt import BCRYPTPasswordManager


def check_pw(hashed_pw, password):
    manager = BCRYPTPasswordManager()
    return manager.check(hashed_pw, password)


USERS = {'editor': 'editor',
         'admin': 'admin',
         'viewer': 'viewer'}

GROUPS = {'editor': ['g:editors'],
          'admin': ['g:admins']}


def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])


class DefaultRoot(object):
    """Base authorizations for all users."""

    __acl__ = [
        (Allow, Everyone, 'view'),
        # (Allow, 'admin', 'edit'),
        # (Allow, 'admin', 'create'),
        (Allow, 'g:editors', 'edit'),
        (Allow, 'g:editors', 'create'),
        (Allow, 'g:admins', ALL_PERMISSIONS)
    ]

    def __init__(self, request):
        """Initialize class."""
        self.request = request


# class EntryRoot(object):

#     __name__ = 'entry'

#     @property
#     def __parent__(self):
#         return DefaultRoot(self.request)

#     def __init__(self, request):
#         self.request = request

#     def __getitem__(self, name):
#         entry_obj = Entry.by_id(name)
#         if entry_obj is None:
#             raise KeyError(name)
#         entry_obj.__parent__ = self
#         return entry_obj
