# -*- coding: utf-8 -*-
import pytest
from sqlalchemy import create_engine
from learning_journal.models import DBSession, Base
from pyramid import testing


# TEST_DATABASE_URL = "postgres://titan:password@localhost:5432/learning_journal" # DO NOT USE EVER.
TEST_DATABASE_URL = "sqlite:////tmp/database.sqlite3"


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
