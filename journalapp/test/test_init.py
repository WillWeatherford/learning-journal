# -*- coding: utf-8 -*-
"""Test that initializedb runs when called."""
import pytest
from journalapp.scripts.initializedb import main


def test_main(config_uri, test_database_url, dbtransaction):
    """Test that main runs."""
    main(['initialize_db',
          config_uri,
          'sqlalchemy.url={}'.format(test_database_url)])


def test_main_error():
    """Test that main does not run without an .ini file."""
    with pytest.raises(SystemExit):
        main(['initialize_db'])
