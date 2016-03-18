"""Define WTForm classes for adding and editing Entries into database."""

from wtforms.validators import Length, InputRequired
from wtforms import Form, StringField, TextAreaField


class EntryForm(Form):
    """Form used for both adding and editing Entry models."""

    title = StringField(
        'Title',
        [Length(max=255, message='Your title is too long.'),
         InputRequired(message='Title is required.')
         ])
    text = TextAreaField(
        'Text',
        [InputRequired(message='Text is required.')
         ])


