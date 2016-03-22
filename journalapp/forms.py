# -*- coding: utf-8 -*-

"""Define WTForm classes for adding and editing Entries into database."""

from wtforms.validators import Length, InputRequired
from wtforms import (
    Form,
    StringField,
    TextAreaField,
    PasswordField,
    ValidationError
)

from .models import DBSession, Entry


def unique_title(form, field):
    """Raise ValidationError if Entry with given title field already exists."""
    title = form.title.data
    existing_entries = DBSession.query(Entry).filter(Entry.title == title)
    if existing_entries.count():
        raise ValidationError('An entry with this title already exists.')


EDIT_VALIDATORS = [
    Length(max=255, message='Your title is too long.'),
    InputRequired(message='Title is required.'),
]

ADD_VALIDATORS = EDIT_VALIDATORS + [unique_title]


class EditEntryForm(Form):
    """Form used for both editing Entry models."""

    title = StringField(
        'Title', EDIT_VALIDATORS)
    text = TextAreaField(
        'Text', [InputRequired(message='Text is required.')])


class AddEntryForm(EditEntryForm):
    """Form used for adding Entry models, with a unique title validator."""

    title = StringField(
        'Title', ADD_VALIDATORS)


class LoginForm(Form):
    """Form for logging in user."""

    username = StringField(
        'Username',
        [Length(min=4, max=32),
         InputRequired(message='Username is required.')
         ])
    password = PasswordField(
        'Password',
        [InputRequired(message='Password is required.')
         ])
