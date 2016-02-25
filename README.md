# pytest-ringo
Helper fixtures to test web applications using the Ringo web framework

## Fixtures
This plugin provides the following fixtures:

1. **app** A *TestApp* instance from *webtest* of the application. Scope is "module".
1. **config** The config object used to configure route etc. Scope is "module".
1. **apprequest** A *DummyRequest* from *Pyramid* to be used to call views. No scope.

## Helpers
This plugin provides the following helper methods. Please consult the source
to see how  to use the methods:

### Transactions
1. **transaction_begin** Begin a new transaction for a testcase
1. **transaction_rollback** Rollback the currently running transaction

### Usecases
1. **login** Login a given user

### Getting data
1. **get_data** A helper methods to get data from the application using the
   REST API.
1. **search_data** A helper methods to search for a specific item in the
   database using the using the
   REST API.
1. **get_max_id** Get the max id of a table in the database (usefull to get
   the id of the last insererted item) using the REST API.

## Invoke
You need to provide the URL to the .ini file when invoking the pytest command::

    py-test --app-config="path/to/config.ini"
