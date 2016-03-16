"""Testing Model."""
# _*_.utf8_*_
from journalapp.models import Entry, DBSession


def test_create_entry(dbtransaction):
    """Test if model initialized with correct vals."""
    new_entry = Entry(title="testblogpost", text="aaa")
    assert new_entry.id is None
    DBSession.add(new_entry)
    DBSession.flush()
    assert new_entry.id is not None


def test_create_text(dbtransaction):
    """Test if model initialized with correct vals."""
    new_entry = Entry(title="testblogpost", text="aaa")
    DBSession.add(new_entry)
    DBSession.flush()
    assert new_entry.text is not None


def test_create_title(dbtransaction):
    """Test if model initialized with correct vals."""
    new_entry = Entry(title="testblogpost", text="aaa")
    DBSession.add(new_entry)
    DBSession.flush()
    assert new_entry.title is not None


def test_create_created(dbtransaction):
    """Test if model initialized with correct vals."""
    new_entry = Entry(title="testblogpost", text="aaa")
    assert new_entry.created is None
    DBSession.add(new_entry)
    DBSession.flush()
    assert new_entry.created is not None
