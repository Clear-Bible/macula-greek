# Development Guide

## Testing

This repository includes a [`pytest`]() test suite.
All tests in the suite must pass in a branch before a pull request can be merged.
There is a core set of tests that prevent basic regressions.
Additionally, pull requests for new features or fixes are expected to have accompanying unit tests that demonstrate the correctness of the change.

### Writing tests
Ideally, most of the code in a test should focus on asserting conditions, not loading or iterating files.
The test suite in this repository employs some helps to improve the developer experience for test authoring.

#### Available files
Collections of file paths are generate in `test/__init__.py` and are avaialable for testing. These lists can be easily imported like so:

```python
from test import __nodes_files__
from test import __lowfat_files__
from test import __tei_files__
```

#### Parameterized Tests
[`pytest`]() offers decorators that allow a single test to be parameterized across a set of files. This allows us to write a single test that can be applied to all of the files in a dataset. When a failure occurs, [`pytest`]() prints of the condition failure and the parameter that the test failed on. 

Example: this test will run for each file defined in the `__nodes_files__` list:

```python
def test_file_is_valid_xml(nodes_file):
  @pytest.mark.parametrize("nodes_file", __nodes_files__)
  ```
    assert etree.parse(nodes_file)

#### Additional Helpers

##### `run_xpath_for_file`

Takes an xpath expression and a file path. 
Returns a list of elements matched by the expression.

### Running the test suite locally

Prerequisites:

* Python 3.x
* Poetry (dependency management for python)

In the project root, install dependencies:

```cli
poetry install
```

Run all tests:

```cli
poetry run pytest
```

Run a specific test file:

```cli
poetry run pytest test/test_lowfat.py 
```

Run the tests with console output:

```cli
poetry run pytest -rP 
```
