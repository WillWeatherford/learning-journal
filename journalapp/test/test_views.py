"""Testing views."""
# _*_.utf8_*_
from journalapp.views import list_view, detail_view
from pyramid.testing import DummyRequest
from journalapp.models import DBSession, Entry


def test_list_view(dbtransaction, new_entry):
    """Test that list_view returns a Query of Entries."""
    test_request = DummyRequest()

    response_dict = list_view(test_request)
    entries = response_dict['entries']
    assert entries[0] == new_entry


def test_list_route(dbtransaction, app, new_entry):
    """Test if model initialized with correct vals."""
    response = app.get('/')
    assert response.status_code == 200


def test_detail_view(dbtransaction, new_entry):
    """Test that list_view returns a Query of Entries."""
    test_request = DummyRequest()
    test_request.matchdict = {'detail_id': new_entry.id}

    response_dict = detail_view(test_request)
    assert response_dict['entry'] == new_entry


def test_detail_route(dbtransaction, app, new_entry):
    """Test if model initialized with correct vals."""
    new_entry_id = new_entry.id
    response = app.get('/detail/{}'.format(new_entry_id))
    assert response.status_code == 200


def test_list_detail(dbtransaction, new_entry):
    """Combine tests of list and detail views."""
    test_request = DummyRequest()

    list_response_dict = list_view(test_request)
    entry = list_response_dict['entries'][0]

    test_request.matchdict = {'detail_id': entry.id}
    entry_response_dict = detail_view(test_request)
    assert entry_response_dict['entry'] == entry == new_entry


def test_add(dbtransaction, app):
    """Test that add view creates a new Entry in database."""
    results = DBSession.query(Entry).filter(
        Entry.title == 'TEST' and Entry.text == 'TEST')
    assert results.count() == 0
    params = {
        'title': 'TEST',
        'text': 'TEST'
    }
    app.post('/add', params=params, status='3*')
    results = DBSession.query(Entry).filter(
        Entry.title == 'TEST' and Entry.text == 'TEST')
    assert results.count() == 1


# def test_edit(dbtransaction, app, new_entry):
#     """Test that edit view can edit an exiting Entry."""
#     new_title = new_entry.title + 'TEST'
#     new_text = new_entry.text + 'TEST'
#     params = {
#         'title': new_title,
#         'text': new_text
#     }
#     app.post('/edit/{}'.format(new_entry.id), params=params, status='3*')
#     # results = DBSession.query(Entry).filter(
#     #     Entry.title == new_title and Entry.text == new_text)
#     # assert results.count() == 1
#     assert new_entry.text == new_text
#     assert new_entry.title == new_title
