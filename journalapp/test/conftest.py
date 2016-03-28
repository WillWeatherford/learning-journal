# -*- coding: utf-8 -*-
"""Configure fixtures for unit and functional tests."""
import os
import pytest
from webob import multidict
from sqlalchemy import create_engine
from pyramid import testing
from journalapp.models import DBSession, Base, Entry


TEST_DATABASE_URL = 'sqlite:////tmp/test_db.sqlite'


@pytest.fixture(scope='session')
def good_login_params():
    """Create correct login information."""
    return {'username': 'admin', 'password': 'secret'}


@pytest.fixture(scope='session')
def test_database_url():
    """Establish test database url as a fixture for entire session."""
    return TEST_DATABASE_URL


@pytest.fixture(scope='session')
def config_uri():
    """Establish configuration uri for initialization."""
    parent_dir = os.path.dirname(__file__)
    gparent_dir = os.path.dirname(parent_dir)
    ggparent_dir = os.path.dirname(gparent_dir)
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


@pytest.fixture()
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


@pytest.fixture()
def app(request, test_database_url, config_uri, good_login_params):
    """Create pretend app fixture of our main app."""
    from journalapp import main
    from webtest import TestApp
    from pyramid.paster import get_appsettings
    settings = get_appsettings(config_uri)
    settings['sqlalchemy.url'] = test_database_url
    app = main({}, **settings)
    test_app = TestApp(app)

    def teardown():
        test_app.post('/login', params=good_login_params, status='3*')
        test_app.get('/delete_all')

    request.addfinalizer(teardown)
    return test_app


@pytest.fixture()
def new_entry(request):
    """Return a fresh new Entry and flush to the database."""
    entry = Entry(title="testblogpost", text="aaa")
    DBSession.add(entry)
    DBSession.flush()

    def teardown():
        DBSession.query(Entry).filter_by(id=entry.id).delete()

    request.addfinalizer(teardown)
    return entry


@pytest.fixture()
def dummy_request():
    """Make a base generic dummy request to be used."""
    request = testing.DummyRequest()
    config = testing.setUp()
    config.add_route('list', '/')
    config.add_route('detail', '/detail/{entry_id}')
    config.add_route('add', '/add')
    config.add_route('edit', '/edit/{entry_id}')
    return request


@pytest.fixture()
def dummy_get_request(dummy_request):
    """Make a dummy GET request to test views."""
    dummy_request.method = 'GET'
    dummy_request.POST = multidict.NoVars()
    return dummy_request


@pytest.fixture()
def dummy_post_request(request, dummy_request):
    """Make a dummy POST request to test views."""
    dummy_request.method = 'POST'
    dummy_request.POST = multidict.MultiDict([('title', 'TESTadd'),
                                              ('text', 'TESTadd')])

    def teardown():
        DBSession.query(Entry).filter(Entry.title == 'TESTadd').delete()

    request.addfinalizer(teardown)
    return dummy_request


@pytest.fixture()
def auth_env(good_login_params):
    """Set username and password into os environment."""
    from cryptacular.bcrypt import BCRYPTPasswordManager
    manager = BCRYPTPasswordManager()
    os.environ['AUTH_USERNAME'] = good_login_params['username']
    os.environ['AUTH_PASSWORD'] = manager.encode(good_login_params['password'])


@pytest.fixture()
def authenticated_app(app, auth_env, good_login_params):
    """Create a version of the app with an authenticated user."""
    app.post('/login', params=good_login_params, status='3*')
    return app


TEST_PARAMS = {
    'title': 'TEST',
    'text': 'TEST'
}


@pytest.fixture()
def authenticated_app_one_entry(authenticated_app, auth_env):
    """Create a version of app with authenticated user and one Entry."""
    authenticated_app.post('/add', params=TEST_PARAMS, status='3*')
    return authenticated_app


@pytest.fixture()
def unauthenticated_app_one_entry(authenticated_app_one_entry):
    """Create a version of app with unauthenticated user and one Entry."""
    authenticated_app_one_entry.get('/logout', status='3*')
    return authenticated_app_one_entry
