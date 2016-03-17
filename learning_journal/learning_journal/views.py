from pyramid.response import Response
from pyramid.view import view_config
import transaction
import datetime

from sqlalchemy.exc import DBAPIError, ResourceClosedError

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
    return {"message": str(display[2]), "header": display[0], "title": display[1], "time": display[3]}


@view_config(route_name='edit', renderer='templates/edit.jinja2')
def edit_view(request):
    id_ = request.matchdict.get('entry_id')
    display = DBSession().query(Entry.metadata.tables['entries']).filter_by(id=id_).one()
    return {"message": str(display[2]), "header": display[0], "title": display[1], "time": display[3]}


@view_config(route_name='add_entry', renderer='templates/edit.jinja2')
def add_view(request):

    title = request.POST.get('title')
    text = request.POST.get('entry_text')
    if title is not None and text is not None:
        session = DBSession()
        new_model = Entry(title=title, text=text)
        session.add(new_model)
        session.flush()
        transaction.commit()
        # input(title, text)
    # New Entry()
    # DBSession.add
    # DBSession.flush
    # Transaction.commit
    return {"time": datetime.datetime.utcnow()}


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
