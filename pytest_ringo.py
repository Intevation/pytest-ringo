#!/usr/bin/env python
# encoding: utf-8

import os
import pytest
from paste.deploy.loadwsgi import appconfig
from mock import Mock
from pyramid import testing
from pyramid.registry import Registry
from webtest import TestApp


@pytest.fixture()
def config(_registry, apprequest):
    config = testing.setUp(_registry, request=apprequest)
    return config


@pytest.fixture(scope="session")
def _registry(app_config):
    name = app_config.context.distribution.project_name
    registry = Registry(name)
    registry.settings = app_config
    return registry


@pytest.fixture(scope="session")
def app(app_config):
    name = app_config.context.distribution.project_name
    app = __import__(name).main({}, **app_config)
    return TestApp(app)


@pytest.fixture()
def apprequest(dbsession):
    from ringo.lib.cache import Cache
    request = testing.DummyRequest()
    request.cache_item_modul = Cache()
    request.cache_item_list = Cache()

    user = Mock()
    user.news = []
    user.settings = {'searches': {'foo': 'bar'}}

    request.user = user

    request.accept_language = Mock(return_value="en")
    request.translate = lambda x: x
    request.db = dbsession
    request.context = Mock()
    request.session.get_csrf_token = lambda: "xxx"
    return request


@pytest.fixture(scope="session")
def app_config(request):
    config = request.config.getoption("--app-config")
    if config:
        return appconfig('config:' + os.path.abspath(config))
    else:
        return None


def pytest_addoption(parser):
    parser.addoption("--app-config", action="store",
                     default=None,
                     help="Path to the application config file")
