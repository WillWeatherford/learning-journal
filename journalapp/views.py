from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Entry,
)


@view_config(route_name='list', renderer='templates/list.jinja2')
def list(request):
    try:
        entries = DBSession.query(Entry).order_by(Entry.created.desc())
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    # import pdb; pdb.set_trace()
    return {'entries': entries}


@view_config(route_name='detail', renderer='templates/detail.jinja2')
def detail(request):
    detail_id = request.matchdict['detail_id']
    entry = DBSession.query(Entry).filter(Entry.id == detail_id).one()
    return {'entry': entry}


conn_err_msg = """\
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

