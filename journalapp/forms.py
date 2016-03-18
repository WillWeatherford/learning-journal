from wtforms.validators import Length, InputRequired
from wtforms import Form, StringField, TextAreaField

class EntryForm(Form):
    title = StringField('Title')
    text = TextAreaField('Text')
