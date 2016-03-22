from wtforms import Form, StringField, TextAreaField, validators
from wtforms import HiddenField

# remove excess whitespace around input text
strip_filter = lambda x: x.strip() if x else None

class EntryCreateForm(Form):
    title = StringField('title', [validators.Length(min=1, max=128)],
                        filters=[strip_filter])
    text = TextAreaField('text', [validators.Length(min=1)],
                         filters=[strip_filter])

class EntryUpdateForm(EntryCreateForm):
    id = HiddenField()
