"""Testing views."""
# _*_.utf8_*_
import pytest
from journalapp.views import list_view, detail_view
from journalapp.models import Entry, DBSession

from pyramid.testing import DummyRequest


@pytest.fixture(scope='function')
def new_entry(request):
    """Create an Entry object for use in tests."""
    entry = Entry(title="test", text="test")
    DBSession.add(entry)
    DBSession.flush()
    return entry


def test_list_view(dbtransaction, new_entry):
    """Test that list_view returns a Query of Entries."""
    test_request = DummyRequest()

    response_dict = list_view(test_request)
    entries = response_dict['entries']
    assert entries[0] == new_entry


def test_detail_view(dbtransaction, new_entry):
    """Test that list_view returns a Query of Entries."""
    test_request = DummyRequest()
    test_request.matchdict = {'detail_id': new_entry.id}

    response_dict = detail_view(test_request)
    assert response_dict['entry'] == new_entry


def test_list_detail(dbtransaction, new_entry):
    """Combine tests of list and detail views."""
    test_request = DummyRequest()

    list_response_dict = list_view(test_request)
    entry = list_response_dict['entries'][0]

    test_request.matchdict = {'detail_id': entry.id}
    entry_response_dict = detail_view(test_request)
    assert entry_response_dict['entry'] == entry == new_entry
