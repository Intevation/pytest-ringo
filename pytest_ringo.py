#!/usr/bin/env python
# encoding: utf-8

import os
import pytest
import json
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
    testing.setUp(registry)
    return registry


@pytest.fixture(scope="session")
def app(app_config):
    name = app_config.context.distribution.project_name
    distribution = __import__(name)
    app = distribution.main({}, **app_config)
    return TestApp(app)


@pytest.fixture()
def apprequest(dbsession, _registry):
    from ringo.lib.cache import Cache
    from ringo.lib.request import RingoRequest
    request = testing.DummyRequest()
    request.ringo = RingoRequest(request)
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


def login(app, username, password, status=302):
    '''Will login the user with username and password. On default we we do
    a check on a successfull login (status 302).'''
    logout(app)
    response = app.post('/auth/login',
        params={'login': username,
                'pass': password},
        status=status
    )
    return response


def logout(app):
    'Logout the currently logged in user (if any)'
    response = app.get('/auth/logout',
        params={},
        status=302
    )
    return response


def transaction_begin(app):
    return app.get("/_test_case/start").follow().follow()


def transaction_rollback(app):
    return app.get("/_test_case/stop").follow().follow()


def get_max_id(app, table):
    result = app.get("/rest/%s" % table)
    data = json.loads(result.json["data"])
    return sorted(data, key=lambda x: int(x["id"]))[-1]["id"]


def get_data(app, table, id=None):
    if id is None:
        result = app.get("/rest/%s" % (table))
        data = json.loads(result.json["data"])
        return data
    else:
        result = app.get("/rest/%s/%s" % (table, id))
        data = json.loads(result.json["data"])[0]
        return data


def search_data(app, table, where, value):
    data = get_data(app, table)
    found = []
    for item in data:
        if item.get(where) == value:
            found.append(item)
    if len(found) > 1:
        return found
    elif len(found) == 1:
        return found[0]
    else:
        return None


@pytest.fixture(scope="session")
def app_config(request):
    config = request.config.getoption("--app-config")
    if config:
        return appconfig('config:' + os.path.abspath(config))
    else:
        return None


def pytest_addoption(parser):
    parser.addoption("--app-config", action="store",
                     default="test.ini",
                     help="Path to the application config file")
