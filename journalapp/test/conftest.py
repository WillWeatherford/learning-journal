# -*- coding: utf-8 -*-
import os
import pytest
from sqlalchemy import create_engine

from journalapp.models import DBSession, Base

# use these to initialize the app for testing
from pyramid.paster import get_appsettings


TEST_DATABASE_URL = 'sqlite:////tmp/test_db.sqlite'
CONFIG_URI = os.path.join('..', '..', 'development.ini')


@pytest.fixture()
def app(DBSession):
    from journalapp import main
    from webtest import TestApp
    # settings = get_appsettings(CONFIG_URI)
    app = main()
    return TestApp(app)


@pytest.fixture(scope='session')
def sqlengine(request):
    engine = create_engine(TEST_DATABASE_URL)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    def teardown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture()
def dbtransaction(request, sqlengine):
    connection = sqlengine.connect()
    transaction = connection.begin()
    DBSession.configure(bind=connection)

    def teardown():
        transaction.rollback()
        connection.close()
        DBSession.remove()

    request.addfinalizer(teardown)

    return connection
