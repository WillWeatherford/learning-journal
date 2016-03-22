# -*- coding: utf-8 -*-
"""SQLAlchemy views to render learning journal."""
from jinja2 import Markup
# from cryptacular.bcrypt import BCRYPTPasswordManager

from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.security import remember, forget
from pyramid.view import view_config

from .models import DBSession, Entry
from .forms import EditEntryForm, AddEntryForm, LoginForm
from .security import check_pw
import markdown


@view_config(route_name='list',
             renderer='templates/list.jinja2',
             permission='view')
def list_view(request):
    """Return rendered list of entries for journal home page."""
    entries = DBSession.query(Entry).order_by(Entry.created.desc())
    return {'entries': entries}


@view_config(route_name='detail',
             renderer='templates/detail.jinja2',
             permission='view')
def detail_view(request):
    """Return rendered single entry for entry detail page."""
    entry_id = request.matchdict['entry_id']
    entry = DBSession.query(Entry).get(entry_id)
    if not entry:
        return Response('Post {} does not exist.'.format(entry_id),
                        content_type='text/plain',
                        status_int=404)
    return {'entry': entry}


@view_config(route_name='add',
             renderer='templates/add-edit.jinja2',
             permission='create')
def add_entry(request):
    """Display a empty form, when submitted, return to the detail page."""
    form = AddEntryForm(request.POST)
    if request.method == "POST" and form.validate():
        new_entry = Entry(title=form.title.data, text=form.text.data)
        DBSession.add(new_entry)
        DBSession.flush()
        next_url = request.route_url('detail', entry_id=new_entry.id)
        return HTTPFound(location=next_url)
    return {'form': form}


@view_config(route_name='edit',
             renderer='templates/add-edit.jinja2',
             permission='edit')
def edit_entry(request):
    """Display editing page to edit entries, return to detail page."""
    entry_id = request.matchdict['entry_id']
    entry = DBSession.query(Entry).get(entry_id)
    if not entry:
        return Response('Post {} does not exist.'.format(entry_id),
                        content_type='text/plain',
                        status_int=404)
    form = EditEntryForm(request.POST, entry)
    if request.method == "POST" and form.validate():
        form.populate_obj(entry)
        DBSession.add(entry)
        DBSession.flush()
        next_url = request.route_url('detail', entry_id=entry.id)
        return HTTPFound(location=next_url)
    return {'form': form}


@view_config(route_name='login',
             renderer='templates/login.jinja2',
             permission='view')
def login(request):
    """Log user in."""
    form = LoginForm(request.POST)
    if request.method == 'POST' and form.validate():
        username = request.params['username']
        password = request.params['password']

        settings = request.registry.settings

        real_username = settings.get('auth.username', '')
        hashed_pw = settings.get('auth.password', '')

        if username == real_username:
            if check_pw(hashed_pw, password):
                headers = remember(request, username)
                return HTTPFound(location=request.route_url('list'),
                                 headers=headers)
            else:
                form.password.errors.append('Invalid password.')
        else:
            form.password.errors.append('Invalid username.')
    return {'form': form}


@view_config(route_name='logout',
             renderer='templates/logout.jinja2',
             permission='view')
def logout(request):
    """Log user out."""
    forget(request)
    return {}


def render_markdown(content, linenums=False, pygments_style='default'):
    """Jinja2 filter to render markdown text. Copied but no understood."""
    ext = "codehilite(linenums={linenums}, pygments_style={pygments_style})"
    output = Markup(
        markdown.markdown(
            content,
            extensions=[ext.format(**locals()), 'fenced_code'])
    )
    return output
