from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .security import DefaultRoot
from .models import (
    DBSession,
    Base,
)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(
        settings=settings,
        authentication_policy=AuthTktAuthenticationPolicy(
            'seekrit',
            hashalg='sha512'
        ),
        authorization_policy=ACLAuthorizationPolicy(),
        root_factory=DefaultRoot,
    )
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('list', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('add_entry', '/create')
    config.add_route('detail', '/view/{entry_id}')
    config.add_route('edit', '/edit/{entry_id}')

    config.scan()
    return config.make_wsgi_app()
