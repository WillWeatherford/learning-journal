"""Set up security standards for the journal app."""
# from .models import Entry
from pyramid.security import Allow, Everyone, ALL_PERMISSIONS
from cryptacular.bcrypt import BCRYPTPasswordManager
from wtforms.ext.csrf.form import SecureForm
from hashlib import md5


SECRET_KEY = 'supersecret'


def check_pw(hashed_pw, password):
    """Return True if provided hash matches against the provided password."""
    manager = BCRYPTPasswordManager()
    return manager.check(hashed_pw, password)


USERS = {'editor': 'editor',
         'admin': 'admin',
         'viewer': 'viewer'}

GROUPS = {'editor': ['g:editors'],
          'admin': ['g:admins']}


def groupfinder(userid, request):
    """Help the TktAuthenticator to find users and their permissions."""
    if userid in USERS:
        return GROUPS.get(userid, [])


class DefaultRoot(object):
    """Base authorizations for all users."""

    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, 'g:editors', 'edit'),
        (Allow, 'g:editors', 'create'),
        (Allow, 'g:admins', ['edit', 'create', 'delete']),
        (Allow, 'g:admins', ALL_PERMISSIONS)
    ]

    def __init__(self, request):
        """Initialize class."""
        self.request = request


class TotesSecureForm(SecureForm):
    """Secure form subclass with CSRF protection."""

    def generate_csrf_token(self, csrf_context):
        """Generate a CSRF Token."""
        text = SECRET_KEY + csrf_context
        token = md5(text.encode('utf-8')).hexdigest()
        return token

    def validate_csrf_token(self, field):
        """Validate a given CSRF token."""
        if field.data != field.current_token:
            raise ValueError('Invalid CSRF')
