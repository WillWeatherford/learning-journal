"""Testing routes through TestApp app fixture.

Tests are designed to happen in sequence, only clearing the database after
session is finished.
"""

TEST_PARAMS = {n: {'title': 'TEST{}'.format(n), 'text': 'TEST{}'.format(n)}
               for n in range(4)}


def test_list_route_get(dbtransaction, app):
    """Test if model initialized with correct vals."""
    response = app.get('/')
    assert response.status_code == 200


def test_add_route_get(dbtransaction, app):
    """TEST that  makes sure user can load add page."""
    response = app.get('/add')
    assert response.status_code == 200


def test_add_route_post(dbtransaction, app):
    """Test that add view creates a new Entry in database."""
    response = app.post('/add', params=TEST_PARAMS[0], status='3*')
    assert response.status_code == 302
    loc_parts = response.location.split('/')
    assert loc_parts[-2] == 'detail' and loc_parts[-1].isdigit()


def test_detail_route_get(dbtransaction, app):
    """Test if model initialized with correct vals."""
    response = app.post('/add', params=TEST_PARAMS[1], status='3*')
    new_entry_id = response.location.split('/')[-1]
    response = app.get('/detail/{}'.format(new_entry_id))
    assert response.status_code == 200


def test_edit_route_get(dbtransaction, app):
    """TEST that  makes sure user can load edit page."""
    response = app.post('/add', params=TEST_PARAMS[2], status='3*')
    new_entry_id = response.location.split('/')[-1]
    response = app.get('/edit/{}'.format(new_entry_id))
    assert response.status_code == 200


def test_edit_route_post(dbtransaction, app):
    """Test that edit view can edit an exiting Entry."""
    response1 = app.post('/add', params=TEST_PARAMS[3], status='3*')
    new_entry_id = response1.location.split('/')[-1]
    params = {
        'title': 'EDIT TEST',
        'text': 'EDIT TEST'
    }
    response2 = app.post('/edit/{}'.format(new_entry_id),
                         params=params, status='3*')
    assert response2.status_code == 302
    loc_parts = response2.location.split('/')
    assert loc_parts[-2] == 'detail' and loc_parts[-1].isdigit()
