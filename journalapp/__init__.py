# -*- coding: utf-8 -*-
"""Initiliazes the journalapp in Pyramid."""
import os
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
)


def main(global_config, **settings):
    """Return a Pyramid WSGI application."""
    if not settings.get('sqlalchemy.url', ''):
        database_url = os.environ.get('DATABASE_URL', None)
        if database_url is not None:
            settings['sqlalchemy.url'] = database_url

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('list', '/')
    config.add_route('detail', '/detail/{entry_id}')
    config.add_route('add', '/add')
    config.add_route('edit', '/edit/{entry_id}')
    config.scan()
    return config.make_wsgi_app()
