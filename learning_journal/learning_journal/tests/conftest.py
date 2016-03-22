# -*- coding: utf-8 -*-
import pytest
from sqlalchemy import create_engine
from learning_journal.models import DBSession, Base, Entry
import os
from pyramid import testing


TEST_DATABASE_URL = "postgres://michaelsullivan:password@localhost:5432/michaelsullivan"

AUTH_DATA = {'username': 'scotist', 'password': 'haecceitas'}


@pytest.fixture()
def app():
    """Create a dummy app."""
    from learning_journal import main
    from pyramid.paster import get_appsettings
    from webtest import TestApp
    settings = get_appsettings('development.ini')
    settings['sqlalchemy.url'] = TEST_DATABASE_URL
    app = main({}, **settings)
    return TestApp(app)


@pytest.fixture(scope="session")
def sqlengine(request):
    # engine is the connection to the database
    engine = create_engine(TEST_DATABASE_URL)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    def teardown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture()
def dbtransaction(request, sqlengine):
    connection = sqlengine.connect()
    transaction = connection.begin()
    DBSession.configure(bind=connection)

    def teardown():
        transaction.rollback()
        connection.close()
        DBSession.remove()

    request.addfinalizer(teardown)
    return connection


@pytest.fixture()
def dummy_request():
    return testing.DummyRequest()


@pytest.fixture()
def loaded_db(dbtransaction):
    """Instantiate a temporary database. Return one entry."""
    from learning_journal.models import Entry, DBSession
    new_model = Entry(title="Norton", text='waffles')
    DBSession.add(new_model)
    DBSession.flush()
    return new_model


@pytest.fixture(scope='function')
def new_entry(request):
    """Create a fake entry."""
    add_entry = Entry(title='new stuff', text='content')
    DBSession.add(add_entry)
    DBSession.flush()

    def teardown():
        DBSession.query(Entry).filter(Entry.id == add_entry.id).delete()
        DBSession.flush()

    request.addfinalizer(teardown)
    return add_entry


@pytest.fixture()
def auth_env():
    from learning_journal.security import pwd_context
    os.environ['AUTH_USERNAME'] = 'scotist'
    os.environ['AUTH_PASSWORD'] = 'haecceitas'


@pytest.fixture()
def authenticated_app(app, auth_env):
    data = AUTH_DATA
    app.post('/login', data)
    return app
