# -*- coding: utf-8 -*-

from learning_journal.models import Entry, DBSession


def test_create_mymodel_entry(dbtransaction, dummy_request):
    """Test creation of model."""
    new_model = Entry(title="new stuff", text="stuff goes here")
    assert new_model.id is None
    DBSession.add(new_model)
    DBSession.flush()
    assert new_model.id is not None


def test_edit_my_model_entry(dbtransaction, dummy_request):
    """Test editing of model."""
    new_model = Entry(title="new stuff", text="stuff goes here")
    DBSession.add(new_model)
    DBSession.flush()
    edit = "yet more stuff for the place where stuff goes"
    new_model.text = edit
    DBSession.flush()
    assert new_model.text == edit
