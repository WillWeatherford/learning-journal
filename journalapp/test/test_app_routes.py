# -*- coding: utf-8 -*-
"""Testing routes through TestApp app fixture.

Tests are designed to happen in sequence, only clearing the database after
session is finished.
"""
import os


TEST_PARAMS = {n: {'title': 'TEST{}'.format(n), 'text': 'TEST{}'.format(n)}
               for n in range(4)}


def test_get_username(auth_env):
    """Test we can get the username from the os environment."""
    assert os.environ.get('AUTH_USERNAME', None) is not None


def test_get_password(auth_env):
    """Test we can get the password from the os environment."""
    assert os.environ.get('AUTH_PASSWORD', None) is not None


def test_password_is_encrypted(auth_env):
    """Test the password is encrypted."""
    assert os.environ.get('AUTH_PASSWORD', None) != 'secret'


def test_check_pw_success(auth_env):
    """Check successful hashing of correct password."""
    from journalapp.security import check_pw
    hashed_pw = os.environ.get('AUTH_PASSWORD')
    assert check_pw(hashed_pw, 'secret')


def test_check_pw_fail(auth_env):
    """Check successful hashing of incorrect password."""
    from journalapp.security import check_pw
    hashed_pw = os.environ.get('AUTH_PASSWORD')
    assert not check_pw(hashed_pw, 'not secret')


def test_list_get(dbtransaction, app):
    """Test if model initialized with correct vals."""
    response = app.get('/')
    assert response.status_code == 200


def test_login_get(dbtransaction, app):
    """Test if login view can be accessed without permission."""
    response = app.get('/login')
    assert response.status_code == 200


def test_login_post_success(dbtransaction, app, auth_env):
    """Test if login view can be accessed without permission."""
    params = {
        'username': 'admin',
        'password': 'secret'
    }
    response = app.post('/login', params=params, status='3*')
    assert response.status_code == 302


def test_login_post_redirect(dbtransaction, app, auth_env):
    """Test if login view can be accessed without permission."""
    params = {
        'username': 'admin',
        'password': 'secret'
    }
    response = app.post('/login', params=params, status='3*')
    loc_parts = response.location.split('/')
    assert loc_parts[-1] == ''


def test_login_post_auth_tkt(dbtransaction, app, auth_env):
    """Test if login view can be accessed without permission."""
    params = {
        'username': 'admin',
        'password': 'secret'
    }
    response = app.post('/login', params=params, status='3*')
    headers = response.headers
    cookies = headers.getall('Set-Cookie')
    for cookie in cookies:
        if cookie.startswith('auth_tkt'):
            break
    else:
        assert False, "Auth tickets not found."


def test_login_post_fail(dbtransaction, app, auth_env):
    """Test if login view can be accessed without permission."""
    params = {
        'username': 'admin',
        'password': 'not secret'
    }
    response = app.post('/login', params=params)
    assert response.status_code == 200


def test_add_no_permission(dbtransaction, app):
    """Test that add route returns a 403 if not permitted."""
    response = app.get('/add', status='4*')
    assert response.status_code == 403


def test_add_with_permission(dbtransaction, authenticated_app):
    """Test that add route returns a 403 if not permitted."""
    params = {
        'username': 'admin',
        'password': 'secret'
    }
    response2 = authenticated_app.get('/add')
    assert response2.status_code == 200


# def test_add_get(dbtransaction, app):
#     """TEST that  makes sure user can load add page."""
#     response = app.get('/add')
#     assert response.status_code == 200


# def test_add_post(dbtransaction, app):
#     """Test that add view creates a new Entry in database."""
#     response = app.post('/add', params=TEST_PARAMS[0], status='3*')
#     assert response.status_code == 302
#     loc_parts = response.location.split('/')
#     assert loc_parts[-2] == 'detail' and loc_parts[-1].isdigit()


# def test_detail_get(dbtransaction, app):
#     """Test if model initialized with correct vals."""
#     # need to be Authenticated.
#     response = app.post('/add', params=TEST_PARAMS[1], status='3*')
#     new_entry_id = response.location.split('/')[-1]
#     response = app.get('/detail/{}'.format(new_entry_id))
#     assert response.status_code == 200


# def test_edit_get(dbtransaction, app):
#     """TEST that  makes sure user can load edit page."""
#     response = app.post('/add', params=TEST_PARAMS[2], status='3*')
#     new_entry_id = response.location.split('/')[-1]
#     response = app.get('/edit/{}'.format(new_entry_id))
#     assert response.status_code == 200


# def test_edit_post(dbtransaction, app):
#     """Test that edit view can edit an exiting Entry."""
#     response1 = app.post('/add', params=TEST_PARAMS[3], status='3*')
#     new_entry_id = response1.location.split('/')[-1]
#     params = {
#         'title': 'EDIT TEST',
#         'text': 'EDIT TEST'
#     }
#     response2 = app.post('/edit/{}'.format(new_entry_id),
#                          params=params, status='3*')
#     assert response2.status_code == 302
#     loc_parts = response2.location.split('/')
#     assert loc_parts[-2] == 'detail' and loc_parts[-1].isdigit()
