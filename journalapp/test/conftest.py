# -*- coding: utf-8 -*-
"""Configure fixtures for unit and functional tests."""
import os
import pytest
from sqlalchemy import create_engine

from journalapp.models import DBSession, Base, Entry

# use these to initialize the app for testing


TEST_DATABASE_URL = 'sqlite:////tmp/test_db.sqlite'
CONFIG_URI = os.path.join('..', '..', 'development.ini')


@pytest.fixture(scope='session')
def sqlengine(request):
    """Return sql engine."""
    engine = create_engine(TEST_DATABASE_URL)
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
    DBSession.configure(bind=connection)

    def teardown():
        transaction.rollback()
        connection.close()
        DBSession.remove()

    request.addfinalizer(teardown)

    return connection


@pytest.fixture()
def app(dbtransaction):
    """Create pretend app fixture of our main app."""
    from journalapp import main
    from webtest import TestApp
    # from pyramid.paster import get_appsettings
    # settings = get_appsettings(CONFIG_URI)
    app = main({})
    return TestApp(app)


@pytest.fixture(scope='function')
def new_entry(request):
    """Return a fresh new Entry and flush to the database."""
    new_entry = Entry(title="testblogpost", text="aaa")
    DBSession.add(new_entry)
    DBSession.flush()

    def teardown():
        DBSession.query(Entry).filter(Entry.id == new_entry.id).delete()
        DBSession.flush()

    request.addfinalizer(teardown)
    return new_entry
