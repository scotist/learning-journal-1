from pyramid.response import Response
from pyramid.view import view_config
import transaction
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


# @view_config(route_name='list', renderer='string')
@view_config(route_name='list', renderer='templates/pretty.jinja2')
def list_view(request):
    display = DBSession().query(Entry.metadata.tables['entries']).all()[::-1][:10]
    return {"content": display, "header": "entries.order_by(latest)[:10]"}


@view_config(route_name='detail', renderer='templates/detail.jinja2')
def detail_view(request):
    id_ = request.matchdict.get('entry_id')
    display = DBSession().query(Entry.metadata.tables['entries']).filter_by(id=id_).one()
    md = markdown.Markdown()
    message = md.convert(display[2])

    return {"message": message, "header": display[0], "title": display[1], "time": display[3]}


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
        transaction.commit()
        return HTTPFound(location='/view/{}'.format(entry_id))
    return {'message': text, 'id': id_, 'title': title, 'time': time}

    # display = DBSession().query(Entry.metadata.tables['entries']).filter_by(id=id_).one()
    # return {"message": str(display[2]), "header": "<input name=\'id\' value=\'{}\'/>".format(display[0]), "title": display[1], "time": display[3]}


@view_config(route_name='add_entry', renderer='templates/edit.jinja2')
def add_view(request):

    form = EntryCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        session = DBSession()
        entry = Entry(title=form.title.data, text=form.text.data)
        session.add(entry)
        session.flush()
        transaction.commit()
        return HTTPFound(location="/")
    return {"time": datetime.datetime.utcnow()}


# def render_markdown(content, linenums=False, pygments_style='default'):
#     md = markdown.Markdown()
#     product = Markup(md.convert(content))
#     return product


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_learning_journal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
