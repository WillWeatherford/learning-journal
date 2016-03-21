# -*- coding: utf-8 -*-
"""Testing views by calling the views functions directly."""

from journalapp.views import (
    list_view,
    detail_view,
    add_entry,
    edit_entry,
)

from journalapp.forms import EditEntryForm, AddEntryForm


def test_list_view(dbtransaction, new_entry, dummy_get_request):
    """Test that list_view returns a Query of Entries."""
    response_dict = list_view(dummy_get_request)
    entries = response_dict['entries']
    assert entries[0] == new_entry


def test_detail_view(dbtransaction, new_entry, dummy_get_request):
    """Test that detail_view returns the correct Entry page."""
    dummy_get_request.matchdict = {'entry_id': new_entry.id}
    response_dict = detail_view(dummy_get_request)
    assert response_dict['entry'] == new_entry


def test_add_view(dbtransaction, dummy_get_request):
    """Test that the add_view returns a dict containing the proper form."""
    response_dict = add_entry(dummy_get_request)
    form = response_dict.get('form', None)
    assert isinstance(form, AddEntryForm)


def test_edit_view(dbtransaction, new_entry, dummy_get_request):
    """Test that the add_view returns a dict containing the proper form."""
    dummy_get_request.matchdict = {'entry_id': new_entry.id}
    response_dict = edit_entry(dummy_get_request)
    form = response_dict.get('form', None)
    assert isinstance(form, EditEntryForm)


def test_edit_view_post(dbtransaction, new_entry, dummy_post_request):
    """Test that the add_view returns a dict containing the proper form."""
    entry_id = new_entry.id
    dummy_post_request.path = '/edit'
    dummy_post_request.matchdict = {'entry_id': entry_id}
    response = edit_entry(dummy_post_request)
    assert response.status_code == 302 and response.title == 'Found'
    loc_parts = response.location.split('/')
    assert loc_parts[-2] == 'detail' and int(loc_parts[-1]) == entry_id


def test_add_view_post(dbtransaction, dummy_post_request):
    """Test that the add_view returns a dict containing the proper form."""
    dummy_post_request.path = '/add'
    response = add_entry(dummy_post_request)
    assert response.status_code == 302 and response.title == 'Found'
    loc_parts = response.location.split('/')
    assert loc_parts[-2] == 'detail' and loc_parts[-1].isdigit()


def test_add_view_dupe(dbtransaction, dummy_post_request):
    """Test that the add_view returns a dict containing the proper form."""
    dummy_post_request.path = '/add'
    response1 = add_entry(dummy_post_request)
    assert response1.status_code == 302 and response1.title == 'Found'
    response2 = add_entry(dummy_post_request)
    assert isinstance(response2, dict) and response2['form'].title.errors


def test_detail_error(dbtransaction, dummy_get_request):
    """Test that detail page gives a 404 when entry ID does not exist."""
    dummy_get_request.matchdict = {'entry_id': 9999}
    response = detail_view(dummy_get_request)
    assert response.status_code == 404


def test_edit_error(dbtransaction, dummy_get_request):
    """Test that edit page gives a 404 when entry ID does not exist."""
    dummy_get_request.matchdict = {'entry_id': 9999}
    response = edit_entry(dummy_get_request)
    assert response.status_code == 404
