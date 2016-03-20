# -*- coding: utf-8 -*-
"""Configure fixtures for unit and functional tests."""
import os
import pytest
from webob import multidict
from sqlalchemy import create_engine
from pyramid.testing import DummyRequest
from journalapp.models import DBSession, Base, Entry

# use these to initialize the app for testing


TEST_DATABASE_URL = 'sqlite:////tmp/test_db.sqlite'


@pytest.fixture(scope='session')
def test_database_url():
    """Establish test database url as a fixture for entire session."""
    return TEST_DATABASE_URL


@pytest.fixture(scope='session')
def config_uri():
    """Establish configuration uri for initialization."""
    parent_dir = os.path.dirname(__file__)
    gparent_dir = os.path.join(parent_dir, '..')
    ggparent_dir = os.path.join(gparent_dir, '..')
    return os.path.join(ggparent_dir, 'development.ini')


@pytest.fixture(scope='session')
def sqlengine(request, test_database_url):
    """Return sql engine."""
    engine = create_engine(test_database_url)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    def teardown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture(scope='session')
def dbtransaction(request, sqlengine):
    """Create database transaction connection."""
    connection = sqlengine.connect()
    transaction = connection.begin()
    DBSession.configure(bind=connection, expire_on_commit=False)

    def teardown():
        transaction.rollback()
        connection.close()
        DBSession.remove()

    request.addfinalizer(teardown)

    return connection


@pytest.fixture(scope='session')
def app(test_database_url, dbtransaction, config_uri):
    """Create pretend app fixture of our main app."""
    from journalapp import main
    from webtest import TestApp
    from pyramid.paster import get_appsettings
    settings = get_appsettings(config_uri)
    settings['sqlalchemy.url'] = test_database_url
    app = main({}, **settings)
    return TestApp(app)


@pytest.fixture(scope='function')
def new_entry(request):
    """Return a fresh new Entry and flush to the database."""
    entry = Entry(title="testblogpost", text="aaa")
    DBSession.add(entry)
    DBSession.flush()

    def teardown():
        DBSession.query(Entry).filter(Entry.id == entry.id).delete()
        # DBSession.flush()

    request.addfinalizer(teardown)
    return entry


@pytest.fixture(scope='function')
def dummy_get_request():
    """Make a dummy GET request to test views."""
    request = DummyRequest()
    request.method = 'GET'
    request.POST = multidict.NoVars()
    return request


@pytest.fixture(scope='function')
def dummy_post_request():
    """Make a dummy POST request to test views."""
    request = DummyRequest()
    request.method = 'POST'
    return request
