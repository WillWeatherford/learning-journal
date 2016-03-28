"""Tests  script to retrieve data from Cris Ewing's existing journal data."""
import pytest
from journalapp.models import Entry, DBSession


EXPECTED_FIELDS = ('id', 'title', 'text', 'markdown', 'created', 'author')


@pytest.fixture(scope='session')
def key():
    """API key to be used by other tests."""
    from journalapp.scripts.get_crisewing_api import get_api_key
    return get_api_key()


@pytest.fixture(scope='session')
def response(key):
    """Generate API response fixture to be used in further tests."""
    from journalapp.scripts.get_crisewing_api import get_api_response
    return get_api_response(key)


@pytest.fixture(scope='session')
def response_list(response):
    """List of entries from JSON response."""
    return response.json()


@pytest.fixture(params=response_list(response(key())))
def entry_dict(request):
    """Establish per-function fixture for individual tests per dict."""
    return request.param


@pytest.fixture(params=EXPECTED_FIELDS)
def expected_field(request):
    """Establish per-function fixture for one test per expected field."""
    return request.param


def test_get_key(key):
    """Test that the API key can be gotten from the os environ."""
    assert key


def test_response_ok(response):
    """Test that API responds with 200 OK."""
    assert response.ok and response.status_code == 200


def test_response_format(response):
    """Test that API response is of the proper content type and encoding."""
    c_type, encoding = response.headers['Content-Type'], response.encoding
    assert c_type == 'application/json; charset=UTF-8' and encoding == 'UTF-8'


def test__num_entries(response_list):
    """Test that the API returns the expected number of prior entries."""
    assert len(response_list) == 18


def test_data_correct(entry_dict, expected_field):
    """Test that all expected fields exist in each JSON entry object."""
    assert entry_dict.get(expected_field, False)


def test_author_data_correct(entry_dict):
    """Test that all expected fields exist in each JSON author object."""
    from journalapp.scripts.get_crisewing_api import is_mine
    assert is_mine(entry_dict)


def test_db_clear(dbtransaction):
    """Make sure that tests are starting from a blank database each time."""
    assert DBSession.query(Entry).count() == 0


def test_one_entry_model(response_list, dbtransaction):
    """Test that Entry model assembles correctly from an entry from API."""
    from journalapp.scripts.get_crisewing_api import (
        entries_from_list, add_entries_to_db)
    new_entries = entries_from_list(response_list[:1])
    result = add_entries_to_db(new_entries, DBSession)
    new_entry = new_entries[0]
    assert all([result == 1,
                new_entry.id is not None,
                new_entry.title is not None,
                new_entry.text is not None,
                new_entry.created is not None])


def test_correct_date(response_list, dbtransaction):
    """Test that Entry model takes formatted time from an entry from API."""
    from journalapp.scripts.get_crisewing_api import (
        entries_from_list, add_entries_to_db, DATETIME_FORMAT)

    new_entries = entries_from_list(response_list[:1])
    add_entries_to_db(new_entries, DBSession)
    new_entry_time = new_entries[0].created.strftime(DATETIME_FORMAT)
    assert new_entry_time == response_list[0]['created']


def test_all_entry_models(response_list, dbtransaction):
    """Test that the full list can be instantiated and added to the DB."""
    from journalapp.scripts.get_crisewing_api import (
        entries_from_list, add_entries_to_db)
    new_entries = entries_from_list(response_list)
    assert add_entries_to_db(new_entries, DBSession) == 18
    assert DBSession.query(Entry).count() == 18


def test_duplicate_entries(response_list, dbtransaction):
    """Test that the full list can be instantiated and added to the DB."""
    from journalapp.scripts.get_crisewing_api import (
        entries_from_list, add_entries_to_db)
    new_entries = entries_from_list(response_list)
    assert add_entries_to_db(new_entries, DBSession) == 18
    new_entries = entries_from_list(response_list)
    assert add_entries_to_db(new_entries, DBSession) == 0
