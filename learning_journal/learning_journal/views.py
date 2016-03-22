from pyramid.response import Response
from pyramid.view import view_config
import datetime
from jinja2 import Markup
import markdown
from sqlalchemy import update
from .forms import EntryCreateForm, EntryUpdateForm
from pyramid.httpexceptions import HTTPFound


from sqlalchemy.exc import DBAPIError, ResourceClosedError, IntegrityError

from .models import (
    DBSession,
    Entry,
)


@view_config(route_name='list', renderer='templates/pretty.jinja2')
def list_view(request):
    display = DBSession.query(Entry).order_by(Entry.created)
    return {"content": display, "header": "entries.order_by(latest)[:10]"}


@view_config(route_name='detail', renderer='templates/detail.jinja2')
def detail_view(request):
    id_ = request.matchdict.get('entry_id')
    entry = DBSession().query(Entry).get(id_)
    # md = markdown.Markdown(safe_mode='replace', html_replacement_text='--RAW HTML NOT ALLOWED--')
    # message = md.convert(entry.text)
    # import pdb; pdb.set_trace()
    message = entry.markdown_text
    return {'entry': entry, 'message': message}



@view_config(route_name='edit', renderer='templates/edit.jinja2')
def edit_view(request):
    id_ = request.matchdict.get('entry_id')
    entry = DBSession().query(Entry).get(id_)
    id_ = entry.id
    title = entry.title
    text = entry.text
    time = entry.created

    form = EntryUpdateForm(request.POST, entry)
    session = DBSession()
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        session.add(entry)
        session.flush()
        entry_id = entry.id
        return HTTPFound(location='/view/{}'.format(entry_id))
    return {'entry': entry}


@view_config(route_name='add_entry', renderer='templates/edit.jinja2')
def add_view(request):

    form = EntryCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        session = DBSession()
        entry = Entry(title=form.title.data, text=form.text.data)
        session.add(entry)
        session.flush()
        return HTTPFound(location="/")
    return {"time": datetime.datetime.utcnow()}
