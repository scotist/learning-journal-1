from wtforms import Form, StringField, TextAreaField, validators
from wtforms import HiddenField

strip_filter = lambda x: x.strip() if x else None


class EntryCreateForm(Form):
    title = StringField('title', [validators.Length(min=1, max=255)])
    text = TextAreaField('text', [validators.Length(min=1)],
                         filters=[strip_filter])


class EntryUpdateForm(EntryCreateForm):
    id = HiddenField()


class LoginForm(Form):
    username = StringField('username', [validators.Length(min=1, max=16)])
    password = StringField('password', [validators.Length(min=1, max=16)])
