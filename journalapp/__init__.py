# -*- coding: utf-8 -*-
"""Initiliazes the journalapp in Pyramid."""
import os
import sys
from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
)

from .security import DefaultRoot, groupfinder


def main(global_config, **settings):
    """Return a Pyramid WSGI application."""
    if not settings.get('sqlalchemy.url', ''):
        database_url = os.environ.get('DATABASE_URL', None)
        if database_url is not None:
            settings['sqlalchemy.url'] = database_url

    try:
        settings['auth.username'] = os.environ['AUTH_USERNAME']
        settings['auth.password'] = os.environ['AUTH_PASSWORD']
        auth_secret = os.environ['JOURNAL_AUTH_SECRET']
    except KeyError:
        print('Autorization global variables have not been set.')
        sys.exit()
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(
        settings=settings,
        authentication_policy=AuthTktAuthenticationPolicy(
            secret=auth_secret,
            hashalg='sha512',
            callback=groupfinder
        ),
        authorization_policy=ACLAuthorizationPolicy(),
        root_factory=DefaultRoot,
    )
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('list', '/')
    config.add_route('detail', '/detail/{entry_id}')
    config.add_route('add', '/add')
    config.add_route('edit', '/edit/{entry_id}')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('logged_out', '/logged_out')
    config.add_route('delete_all', '/delete_all')
    config.add_route('delete_one', '/delete_one/{entry_id}')

    config.scan()
    return config.make_wsgi_app()
