# pytest-ringo
Helper fixtures to test web applications using the Ringo web framework

## Fixtures
This plugin provides the following fixtures:

1. **app** A *TestApp* instance from *webtest* of the application. Scope is "module".
1. **config** The config object used to configure route etc. Scope is "module".
1. **apprequest** A *DummyRequest* from *Pyramid* to be used to call views. No scope.

## Invoke
You need to provide the URL to the .ini file when invoking the pytest command::

    py-test --app-config="path/to/config.ini"
