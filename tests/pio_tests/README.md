# PredictionIO - Integration Tests

This python module introduces a basic framework for adding integration tests to
PredictionIO. It is nothing more than a collection of utility functions mostly being wrappers
over shell executed commands.

### Prerequisites
In order to execute tests, besides a configured **PredictionIO** environment one
has to download the following python-3 packages:
* requests
* unittest
* xmlrunner

Also, set the **$PYTHONPATH** to **$PIO_HOME/tests/** and **$PIO_HOME/tests/pio_tests/**
directories in order to load the python module.

### Execution
*tests.py* - the executable script. Launches eventserver to be available for the tests.
You can pass it arguments to:
* suppress the output of executed shell commands within the tests
* enable logging
* specify which tests should be executed (by names)

You can specify which tests should be executed by passing arguments as below:
```shell
python3 tests.py --tests basic_app_usecases scala_parallel_similarproduct_test
```
* Available test names are specified in *tests.py*
* You don't need to type in the full test name, only the first identifying characters.

For more information run:
```shell
python3 tests.py -h
```

As soon as the tests are finishied an XML file with JUnit-like test reports 
is created in test-reports/ directory.

### Adding new tests
Every test should be an instance of **pio_tests.integration.BaseTestCase** defined in **pio_tests.integration**.  
Upon creation, a **pio_tests.integration.TestContext**  object is provided to it with description of:
* ip address and a port of running eventserver
* directories containing data for specific tests

Every test should be registered in the appropriate place in *tests.py* file, whereas
its definition should reside in **pio_tests.scenarios** module. If the test requires some additional files
during the execution, you should put them under *data* directory mentioned above.

To run tests for the engine, you can provide the engine Github url as *template* argument
for *AppContext* when creating **pio_tests.utility.AppEngine**. AppEngine provides various utility functions
for downloading, building, training, and deploying template engine.

To see examples of implemented tests, refer to files in **scenarios/templates/**,
which replicates QuickStart tutorial for some PredictionIO templates.
