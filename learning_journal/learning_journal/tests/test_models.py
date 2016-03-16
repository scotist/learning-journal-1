# -*- coding: utf-8 -*-

from learning_journal.models import Entry, DBSession


def test_create_mymodel(dbtransaction):
    new_model = Entry(title="Norton", text="waffles")
    assert new_model.id is None
    DBSession.add(new_model)
    DBSession.flush()
    assert new_model.id is not None
