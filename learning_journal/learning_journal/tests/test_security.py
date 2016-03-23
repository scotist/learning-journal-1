# -*- coding: utf-8 -*-
import pytest
import webtest
import os
from learning_journal import main
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from learning_journal.security import check_pw


AUTH_DATA = {'username': 'scotist', 'password': 'haecceitas'}


@pytest.fixture()
def app():
    settings = {'sqlalchemy.url': 'postgres://michaelsullivan:password@localhost:5432/michaelsullivan'}
    app = main({}, **settings)
    return webtest.TestApp(app)


@pytest.fixture()
def auth_env():
    from learning_journal.security import pwd_context
    os.environ['AUTH_PASSWORD'] = pwd_context.encrypt('haecceitas')
    os.environ['AUTH_USERNAME'] = 'scotist'


@pytest.fixture()
def authenticated_app(app, auth_env):
    app.post('/login', AUTH_DATA)
    return app


# def test_no_access_to_view(app):
#     response = app.get('/secure')
#     assert response.status_code == 403


def test_access_to_view(authenticated_app):
    response = authenticated_app.get('/login')
    assert response.status_code == 200


def test_password_exists(auth_env):
    assert os.environ.get('AUTH_PASSWORD', None) is not None


def test_username_exists(auth_env):
    assert os.environ.get('AUTH_USERNAME', None) is not None


def test_check_pw_success(auth_env):
    from learning_journal.security import check_pw
    password = 'haecceitas'
    assert check_pw(password)

def test_check_pw_fails(auth_env):
    from learning_journal.security import check_pw
    password = 'blargles'
    assert not check_pw(password)


def test_stored_password_is_encrypted(auth_env):
    assert os.environ.get('AUTH_PASSWORD', None) != 'haecceitas'


def test_get_login_view(app):
    response = app.get('/login')
    assert response.status_code == 200


def test_post_login_success(app, auth_env):
    response = app.post('/login', AUTH_DATA)
    assert response.status_code == 302


def test_post_login_success_redirects_home(app, auth_env):
    data = {'username': 'scotist', 'password': 'haecceitas'}
    response = app.post('/login', data)
    headers = response.headers
    domain = 'http://localhost'
    actual_path = headers.get('Location', '')[len(domain):]
    assert actual_path == '/'


def test_post_login_success_auth_tkt_present(app, auth_env):
    data = {'username': 'scotist', 'password': 'haecceitas'}
    response = app.post('/login', data)
    headers = response.headers
    cookies_set = headers.getall('Set-Cookie')
    assert cookies_set
    for cookie in cookies_set:
        if cookie.startswith('auth_tkt'):
            break
    else:
        assert False


def test_post_login_fails_bad_password(app, auth_env):
    data = {'username': 'scotist', 'password': 'garbage'}
    response = app.post('/login', data)
    assert response.status_code == 200
