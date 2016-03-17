# -*- coding: utf-8 -*-

from learning_journal.models import Entry, DBSession


def test_create_mymodel(dbtransaction, dummy_request):
    new_model = Entry(title="Norton", text="waffles")
    assert new_model.id is None
    DBSession.add(new_model)
    DBSession.flush()
    assert new_model.id is not None



def test_list_view(dbtransaction, dummy_request):
    from learning_journal.views import list_view
    new_model = Entry(title="Norton", text="waffles")
    DBSession.add(new_model)
    DBSession.flush()
    response_dict = list_view(dummy_request)
    assert response_dict['content'][0][1] == new_model.title


def test_detail_view(dbtransaction, dummy_request):
    from learning_journal.views import detail_view
    new_model = Entry(title="Norton", text="waffles")
    dummy_request.matchdict = {'entry_id': 1}
    DBSession.add(new_model)
    DBSession.flush()
    response_dict = detail_view(dummy_request)
    assert response_dict['message'] == new_model.text
