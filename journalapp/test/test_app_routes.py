# -*- coding: utf-8 -*-
"""Testing routes through TestApp app fixture.

Tests are designed to happen in sequence, only clearing the database after
session is finished.
"""
import os


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


def test_init_no_auth_tkt(dbtransaction, app):
    """Test that the geting the front page of the app has no auth cookies."""
    response = app.get('/')
    response_cookies = response.headers.getall('Set-Cookie')
    auth_tkts = [ck for ck in response_cookies if ck.startswith('auth_tkt')]
    assert not auth_tkts

    request_cookies = response.request.headers.items()
    auth_tkts = [value for cookie, value in request_cookies
                 if cookie == 'Cookie' and value.startswith('auth_tkt')]
    assert not auth_tkts


def test_list_get(dbtransaction, app):
    """Test if model initialized with correct vals."""
    response = app.get('/')
    assert response.status_code == 200


def test_login_get(dbtransaction, app):
    """Test if login view can be accessed without permission."""
    response = app.get('/login')
    assert response.status_code == 200


def test_login_post_success(dbtransaction, app, auth_env, good_login_params):
    """Test if login view can be accessed without permission."""
    response = app.post('/login', params=good_login_params, status='3*')
    assert response.status_code == 302


def test_login_post_redirect(dbtransaction, app, auth_env, good_login_params):
    """Test if login view can be accessed without permission."""
    response = app.post('/login', params=good_login_params, status='3*')
    loc_parts = response.location.split('/')
    assert loc_parts[-1] == ''


def test_login_post_auth_tkt(dbtransaction, app, auth_env, good_login_params):
    """Test if login view can be accessed without permission."""
    response = app.post('/login', params=good_login_params, status='3*')
    response_cookies = response.headers.getall('Set-Cookie')
    auth_tkts = [ck for ck in response_cookies if ck.startswith('auth_tkt')]
    assert auth_tkts


def test_login_post_fail(dbtransaction, app, auth_env):
    """Test if login view can be accessed without permission."""
    bad_params = {
        'username': 'admin',
        'password': 'not secret'
    }
    response = app.post('/login', params=bad_params)
    assert response.status_code == 200


def test_logout(dbtransaction, app):
    """Test that unauthorized user can go to the logout page."""
    response = app.get('/logout', status='3*')
    assert response.status_code == 302


def test_logged_out(dbtransaction, app):
    """Test that unauthorized user can go to the logout page."""
    response = app.get('/logged_out')
    assert response.status_code == 200


def test_logout_no_auth_tkt(dbtransaction, authenticated_app):
    """Test that authenticated app deletes cookies on log out."""
    response = authenticated_app.get('/logout')
    for cookie in response.headers.getall('Set-Cookie'):
        if cookie.startswith('auth_tkt'):
            cookie_parts = dict([tuple(part.split('='))
                                 for part in cookie.split('; ')])
            if cookie_parts['auth_tkt'] != '':
                assert False, "Auth tickets found."
    else:
        assert True, "Auth tickets not found."


def test_add_no_permission(dbtransaction, app):
    """Test that add route returns a 403 if not permitted."""
    response = app.get('/add', status='4*')
    assert response.status_code == 403


def test_add_with_permission(dbtransaction, authenticated_app):
    """Test that add route returns a 200 if authenticated."""
    response = authenticated_app.get('/add')
    assert response.status_code == 200


def test_no_permission_add_link(dbtransaction, app):
    """Test that the "add" link does not show up when not authenticated."""
    response = app.get('/')
    links = response.html.find_all('a')
    for link in links:
        href = link.get('href')
        if href.endswith('/add'):
            assert False, "Add link found when not supposed to be."
    assert True


def test_permission_add_link(dbtransaction, authenticated_app):
    """Test that the "add" link does show up when authenticated."""
    response = authenticated_app.get('/')
    links = response.html.find_all('a')
    for link in links:
        href = link.get('href')
        if href.endswith('/add'):
            break
    else:
        assert False, "Add link found when not supposed to be."


def test_no_permission_can_view(dbtransaction, unauthenticated_app_one_entry):
    """Test that unauthenticated user can still view the detail of an entry."""
    app = unauthenticated_app_one_entry
    response = app.get('/detail/1')
    assert response.status_code == 200


def test_no_permission_edit_link(dbtransaction, unauthenticated_app_one_entry):
    """Test that the "edit" link does not show up when not authenticated."""
    app = unauthenticated_app_one_entry
    response = app.get('/detail/1')
    links = response.html.find_all('a')
    for link in links:
        href = link.get('href')
        if href.endswith('/edit/1'):
            assert False, "edit link found when not supposed to be."
    assert True


def test_permission_edit_link(dbtransaction, authenticated_app_one_entry):
    """Test that the "edit" link does show up when authenticated."""
    app = authenticated_app_one_entry
    response = app.get('/detail/1')
    links = response.html.find_all('a')
    for link in links:
        href = link.get('href')
        if href.endswith('/edit/1'):
            break
    else:
        assert False, "Edit link not found for authorized user."


def test_permission_add_post(dbtransaction, authenticated_app):
    """Test that add view creates a new Entry in database."""
    app = authenticated_app
    params = {
        'title': 'TEST2',
        'text': 'TEST2',
    }
    response = app.post('/add', params=params, status='3*')
    assert response.status_code == 302
    loc_parts = response.location.split('/')
    assert loc_parts[-2] == 'detail' and loc_parts[-1].isdigit()


def test_permission_edit_get(dbtransaction, authenticated_app_one_entry):
    """TEST that  makes sure authenticated user can load edit page."""
    response = authenticated_app_one_entry.get('/edit/1')
    assert response.status_code == 200


def test_no_permission_edit_get(dbtransaction, unauthenticated_app_one_entry):
    """TEST that  makes sure authenticated user can load edit page."""
    response = unauthenticated_app_one_entry.get('/edit/1', status='4*')
    assert response.status_code == 403


def test_edit_post(dbtransaction, authenticated_app_one_entry):
    """Test that edit view can edit an exiting Entry."""
    app = authenticated_app_one_entry
    params = {
        'title': 'EDIT TEST',
        'text': 'EDIT TEST'
    }
    response = app.post('/edit/1', params=params, status='3*')
    assert response.status_code == 302
    loc_parts = response.location.split('/')
    assert loc_parts[-2] == 'detail' and loc_parts[-1].isdigit()
