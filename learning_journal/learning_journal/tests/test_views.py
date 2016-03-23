# -*- coding: utf-8 -*-

from learning_journal.models import Entry, DBSession
from webtest import app as webtestapp
import pytest


def test_list_route(dbtransaction, app):
    """Test if model initialized with correct vals."""
    response = app.get('/')
    assert response.status_code == 200


def test_create_route(dbtransaction, app):
    """Test if permissions block anonymous users."""
    with pytest.raises(webtestapp.AppError):
        app.get('/create')


def test_edit_route(dbtransaction, app):
    """Test if permissions block anonymous users."""
    new_model = Entry(title="scotist", text="haecceitas")
    DBSession.add(new_model)
    DBSession.flush()
    with pytest.raises(webtestapp.AppError):
        app.get('/edit/{}'.format(new_model.id))


def test_list_view(dbtransaction, dummy_request):
    """Test list view function."""
    from learning_journal.views import list_view
    new_model = Entry(title="scotist", text="haecceitas")
    DBSession.add(new_model)
    DBSession.flush()
    response_dict = list_view(dummy_request)
    assert response_dict['content'].one().title == new_model.title


def test_detail_view(dbtransaction, dummy_request):
    """Test detail view function."""
    from learning_journal.views import detail_view
    new_model = Entry(title="scotist", text="haecceitas")
    DBSession.add(new_model)
    DBSession.flush()
    dummy_request.matchdict = {'entry_id': new_model.id}
    response_dict = detail_view(dummy_request)
    assert response_dict['entry'].markdown_text == '<p>haecceitas</p>'
