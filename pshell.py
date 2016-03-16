from webtest import TestApp


def setup(env):
    env['request'].host = '127.0.0.1'
    env['request'].scheme = 'http'
    env['request'] = TestApp(env['app'])
