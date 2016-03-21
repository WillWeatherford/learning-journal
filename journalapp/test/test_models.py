# -*- coding: utf-8 -*-
"""Test that Entry model addition works as expected."""


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
