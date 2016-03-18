"""Testing Model."""
# _*_.utf8_*_
from journalapp.models import Entry, DBSession


def test_create_entry(dbtransaction, new_entry):
    """Test if model initialized with correct vals."""
    assert new_entry.id is not None


def test_create_text(dbtransaction, new_entry):
    """Test if model initialized with correct vals."""
    assert new_entry.text is not None


def test_create_title(dbtransaction, new_entry):
    """Test if model initialized with correct vals."""
    assert new_entry.title is not None


def test_create_created(dbtransaction, new_entry):
    """Test if model initialized with correct vals."""
    assert new_entry.created is not None
