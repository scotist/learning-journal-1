from wtforms import Form, StringField, TextAreaField, validators
from wtforms import HiddenField

strip_filter = lambda x: x.strip() if x else None

class EntryCreateForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=255)],
                        filters=[strip_filter])
    entry = TextAreaField('Contents', [validators.Length(min=1)],
                         filters=[strip_filter])

class EntryUpdateForm(EntryCreateForm):
    id = HiddenField()
