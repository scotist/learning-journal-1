from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError, ResourceClosedError

from .models import (
    DBSession,
    Entry,
)

# @view_config(route_name='list', renderer='string')
@view_config(route_name='list', renderer='templates/base.jinja2')
def list_view(request):
    display = DBSession().query(Entry.metadata.tables['entries']).all()[::-1]
    return {"content": display, "header": "you are at list view!"}


@view_config(route_name='detail', renderer='templates/base.jinja2')
def detail_view(request):
    id_ = request.matchdict.get('entry_id')
    display = DBSession().query(Entry.metadata.tables['entries']).filter_by(id=id_).one()
    return {"message": str(display[2]), "header": "you are view the details!"}


@view_config(route_name='add_entry', renderer='string')
def add_view(request):
    # New Entry()
    # DBSession.add
    # DBSession.flush
    # Transaction.commit
    return "You are adding an entry!"


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
