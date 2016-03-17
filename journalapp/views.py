"""SQLAlchemy views to render learning journal."""
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Entry,
)


@view_config(route_name='list', renderer='templates/list.jinja2')
def list_view(request):
    """Return rendered list of entries for journal home page."""
    try:
        entries = DBSession.query(Entry).order_by(Entry.created.desc())
        return {'entries': entries}
    except DBAPIError:
        return Response(CONN_ERR_MSG,
                        content_type='text/plain',
                        status_int=500)


@view_config(route_name='detail', renderer='templates/detail.jinja2')
def detail_view(request):
    """Return rendered single entry for entry detail page."""
    try:
        detail_id = request.matchdict['detail_id']
        entry = DBSession.query(Entry).get(detail_id)
        return {'entry': entry}
    except DBAPIError:
        return Response(CONN_ERR_MSG,
                        content_type='text/plain',
                        status_int=500)

CONN_ERR_MSG = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_journalapp_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
