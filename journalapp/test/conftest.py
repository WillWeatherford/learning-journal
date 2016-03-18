# -*- coding: utf-8 -*-
import pytest
from sqlalchemy import create_engine

from journalapp.models import DBSession, Base

# use these to initialize the app for testing
# from pyramid.paster import (
#     get_appsettings,
# )


TEST_DATABASE_URL = 'sqlite:////tmp/test_db.sqlite'


# from webtest import TestApp
# create app fixture
# github.com/cewing/learning_journal/blob/master/test_journal.py


@pytest.fixture(scope='session')
def sqlengine(request):
    # use settings from config file
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


@pytest.fixture()
def app(DBSession):
    pass