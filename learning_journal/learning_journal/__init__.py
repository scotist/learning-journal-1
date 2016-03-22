from pyramid.config import Configurator
from sqlalchemy import engine_from_config
import os
from .models import (
    DBSession,
    Base,
    # DefaultRoot,
)
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .security import groupfinder


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    # config = Configurator(
    #     settings=settings,
    #     authentication_policy=authentication_policy,
    #     authorization_policy=authorization_policy,
    #     root)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('list', '/')
    config.add_route('login', '/login')
    config.add_route('add_entry', '/create')
    config.add_route('detail', '/view/{entry_id}')
    config.add_route('edit', '/edit/{entry_id}')

    config.scan()
    return config.make_wsgi_app()
