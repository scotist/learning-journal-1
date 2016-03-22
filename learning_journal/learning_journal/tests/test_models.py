# -*- coding: utf-8 -*-

from learning_journal.models import Entry, DBSession


def test_create_mymodel_entry(dbtransaction, dummy_request):
    """Test creation of model."""
    new_model = Entry(title="Norton", text="waffles")
    assert new_model.id is None
    DBSession.add(new_model)
    DBSession.flush()
    assert new_model.id is not None


def test_create_mymodel_text(dbtransaction, dummy_request):
    """Test text creation of model."""
    new_model = Entry(title="Norton", text="waffles")
    assert new_model.id is None
    DBSession.add(new_model)
    DBSession.flush()
    assert new_model.text == 'waffles'


def test_create_mymodel_title(dbtransaction, dummy_request):
    """Test title creation of model."""
    new_model = Entry(title="Norton", text="waffles")
    assert new_model.id is None
    DBSession.add(new_model)
    DBSession.flush()
    assert new_model.title == 'Norton'


def test_create_mymodel_created(dbtransaction, dummy_request):
    """Test "created" creation of model."""
    new_model = Entry(title="Norton", text="waffles")
    assert new_model.id is None
    DBSession.add(new_model)
    DBSession.flush()
    assert new_model.created is not None
