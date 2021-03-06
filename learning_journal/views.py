from pyramid.view import view_config
import datetime
from .forms import EntryCreateForm, EntryUpdateForm, LoginForm
from pyramid.httpexceptions import HTTPFound, HTTPTemporaryRedirect
from .security import check_pw
from pyramid.security import remember, forget
from .models import (
    DBSession,
    Entry,
)
try:
    from .security import check_pw
except ImportError:
    pass


@view_config(route_name='login', renderer='templates/login.jinja2')
def login_view(request):
    username = request.params.get('username', '')
    password = request.params.get('password', '')
    login_form = LoginForm(username=username, password=password)
    if request.method == 'POST' and login_form.validate():
        if check_pw(password):
            headers = remember(request, userid=username)
            return HTTPFound(location="/", headers=headers)
    return {'form': login_form}


@view_config(route_name='logout', renderer='string')
def logout_view(request):
    """ Log the user out automatically."""
    headers = forget(request)
    # return HTTPTemporaryRedirect(location="/login")
    return HTTPFound(location="/", headers=headers)


@view_config(route_name='list', renderer='templates/list.jinja2')
def list_view(request):
    display = DBSession.query(Entry).order_by(Entry.created)
    return {"content": display, "header": "entries.order_by(latest)[:10]"}


@view_config(route_name='detail', renderer='templates/detail.jinja2')
def detail_view(request):
    id_ = request.matchdict.get('entry_id')
    entry = DBSession().query(Entry).get(id_)
    return {'entry': entry}


@view_config(route_name='edit', renderer='templates/edit.jinja2',
             permission="edit")
def edit_view(request):
    id_ = request.matchdict.get('entry_id')
    entry = DBSession().query(Entry).get(id_)

    form = EntryUpdateForm(request.POST, entry)
    session = DBSession()
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        session.add(entry)
        session.flush()
        entry_id = entry.id
        return HTTPFound(location='/view/{}'.format(entry_id))
    return {'entry': entry}


@view_config(route_name='add_entry', renderer='templates/edit.jinja2',
             permission="edit")
def add_view(request):
    form = EntryCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        session = DBSession()
        entry = Entry(title=form.title.data, text=form.text.data)
        session.add(entry)
        session.flush()
        return HTTPFound(location="/")
    return {"time": datetime.datetime.utcnow()}


@view_config(route_name='delete_entry', renderer='templates/list.jinja2',         permission='edit')
def delete_entry(request):
    entry_id = request.matchdict['entry_id']
    entry = DBSession.query(Entry).get(entry_id)
    DBSession.delete(entry)
    DBSession.flush()
    return HTTPFound(location='/')
