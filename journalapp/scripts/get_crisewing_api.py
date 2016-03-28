"""Script to retrieve existing journal entries in Cris Ewing's database."""

import os
import sys
import requests
from journalapp.scripts import initializedb
from datetime import datetime
from journalapp.models import Entry, DBSession
import transaction

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'


def get_api_key():
    """Return API key from system global environmental variables."""
    key = os.environ.get('CRISEWING_API_KEY')
    if not key:
        print('crisewing API key not found in os.environ.')
        sys.exit()
    return key


def get_api_response(key):
    """Return a Response object from the requests module."""
    url = 'https://sea401d2.crisewing.com/api/export?apikey={}'.format(key)
    return requests.get(url)


def format_datetime(string):
    """Return a datetime object from the proper format."""
    return datetime.strptime(string, DATETIME_FORMAT)


def entries_from_list(entry_list):
    """Return a list of new Entry objects from list of dicts."""
    new_entries = []
    for entry_dict in entry_list:
        if not is_mine(entry_dict):
            continue
        created = format_datetime(entry_dict['created'])
        new_entry = Entry(created=created,
                          title=entry_dict['title'],
                          text=entry_dict['text'])
        new_entries.append(new_entry)
    return new_entries


def is_mine(entry_dict):
    """Make sure that entry is actually mine, just in case."""
    author = entry_dict.get('author', {})
    return all([author.get('username', '') == 'WillWeatherford',
                author.get('display_name', '') == 'Will Weatherford'])


def add_entries_to_db(entries, session):
    """Add the given list of Entry models to the given db session."""
    success_count = 0
    for entry in entries:
        if session.query(Entry).filter_by(title=entry.title).count():
            print('{} is already in the database.'.format(entry.title))
            continue
        session.add(entry)
        session.flush()
        success_count += 1
    return success_count


def main():
    """Run the whole script and put new items into database."""
    if len(sys.argv) < 2:
        print('Config URI argument must be specified.')
        sys.exit()
    initializedb.main()
    key = get_api_key()
    response = get_api_response(key)
    entries_list = response.json()
    entries = entries_from_list(entries_list)
    success_count = add_entries_to_db(entries, DBSession)
    if success_count:
        transaction.commit()
    print('{} entries successfully migrated.'.format(success_count))
