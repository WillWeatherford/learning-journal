"""SQLAlchemy views to render learning journal."""
from jinja2 import Markup
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Entry,
)

from journalapp.forms import EntryForm
import markdown


@view_config(route_name='list', renderer='templates/list.jinja2')
def list_view(request):
    """Return rendered list of entries for journal home page."""
    try:
        entries = DBSession.query(Entry).order_by(Entry.created.desc())
        return {'entries': entries}
    except DBAPIError:
        return Response(DB_ERR_MSG, content_type='text/plain', status_int=500)


@view_config(route_name='detail', renderer='templates/detail.jinja2')
def detail_view(request):
    """Return rendered single entry for entry detail page."""
    try:
        entry_id = request.matchdict['entry_id']
        entry = DBSession.query(Entry).get(entry_id)
        return {'entry': entry}
    except DBAPIError:
        return Response(DB_ERR_MSG, content_type='text/plain', status_int=500)


@view_config(route_name='add', renderer='templates/add-edit.jinja2')
def add_entry(request):
    """Display a empty form, when submitted, return to the detail page."""
    try:
        form = EntryForm(request.POST)
        if request.method == "POST" and form.validate():
            new_entry = Entry(title=form.title.data, text=form.text.data)
            DBSession.add(new_entry)
            DBSession.flush()
            next_url = request.route_url('detail', entry_id=new_entry.id)
            return HTTPFound(location=next_url)
        return {'form': form}
    except DBAPIError:
        return Response(DB_ERR_MSG, content_type='text/plain', status_int=500)


@view_config(route_name='edit', renderer='templates/add-edit.jinja2')
def edit_entry(request):
    """Display editing page to edit entries, return to detail page."""
    try:
        entry_id = request.matchdict['entry_id']
        entry = DBSession.query(Entry).get(entry_id)
        form = EntryForm(request.POST, entry)
        if request.method == "POST" and form.validate():
            form.populate_obj(entry)
            DBSession.add(entry)
            DBSession.flush()
            next_url = request.route_url('detail', entry_id=entry.id)
            return HTTPFound(location=next_url)
        return {'form': form}
    except DBAPIError:
        return Response(DB_ERR_MSG, content_type='text/plain', status_int=500)


def render_markdown(content, linenums=False, pygments_style='default'):
    """Jinja2 filter to render markdown text. Copied but no understood."""
    ext = "codehilite(linenums={linenums}, pygments_style={pygments_style})"
    output = Markup(
        markdown.markdown(
            content,
            extensions=[ext.format(**locals()), 'fenced_code'])
    )
    return output


DB_ERR_MSG = """\
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
