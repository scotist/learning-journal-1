from pyramid.view import view_config
import datetime
from .forms import EntryCreateForm, EntryUpdateForm, LoginForm
from pyramid.httpexceptions import HTTPFound
<<<<<<< HEAD
from .security import check_pw
=======
from pyramid.security import remember, forget
>>>>>>> 199dd29d889a7eddb3b3bed48b624e071f6a698b
from .models import (
    DBSession,
    Entry,
)
try:
    from .secrets import USERNAME, PASSWORD
except ImportError:
    USERNAME = "norton"
    PASSWORD = "password"


@view_config(route_name='login', renderer='templates/login.jinja2')
def login_view(request):
    """ Log the user in automatically.

    The remember object actually returns a header list of tuples containing
    cookie information
    """
    form = LoginForm(request.POST)
    if request.method == 'POST' and form.validate():

        if form.data['username'] == USERNAME and \
           form.data['password'] == PASSWORD:
            headers = remember(request, userid="norton")
            return HTTPFound(location="/", headers=headers)
        else:
            message = "Login Failed"
            color = "red"
    else:
        message = "Please Login"
        color = "green"
    return {"message": message, "color": color}


@view_config(route_name='logout', renderer='string')
def logout_view(request):
    """ Log the user out automatically.

    The remember object actually returns a header list of tuples containing
    cookie information
    """
    headers = forget(request)
    return HTTPFound(location="/", headers=headers)


@view_config(route_name='list', renderer='templates/pretty.jinja2')
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


@view_config(route_name='login', renderer='templates/login.jinja2')
def login_view(request):
    username = request.params.get('username', '')
    password = request.params.get('password', '')
    login_form = LoginForm(username=username, password=password)
    if request.method == 'POST':
        if check_pw(password):
            headers = remember(request, username)
            return HTTPFound(location='/', headers=headers)
    return {'form': login_form}
