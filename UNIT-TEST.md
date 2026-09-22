# Development Guide

## Testing

[`pytest`](https://docs.pytest.org/) is used to run tests to verify data correctness.
All tests in the suite must pass in a branch before a pull request can be merged.
Along with a core set of tests to catch basic regressions,
pull requests for new features or fixes are expected to have accompanying unit tests that demonstrate the correctness of the change.

### Writing tests
In aiming to keep tests readable and succinct, there are some preset patterns and helpers available to those writing tests.

#### Available files
Lists of expected file paths are created in `test/__init__.py`.
Tests can use these expected file paths as test targets.
File path lists can be imported like so:

```python
from test import __nodes_files__
from test import __lowfat_files__
from test import __tei_files__
```

#### Parameterized Tests
[`pytest`](https://docs.pytest.org/) offers decorators that allow a single test to be parameterized across a set of files. This allows us to write a single test that can be applied to all of the files in a dataset. When a failure occurs, [`pytest`]() prints of the condition failure and the parameter that the test failed on.

Example: this test will run for each file defined in the `__nodes_files__` list:

```python
@pytest.mark.parametrize("nodes_file", __nodes_files__)
def test_file_is_valid_xml(nodes_file):
    assert etree.parse(nodes_file)
```

#### Additional Helpers

##### `run_xpath_for_file`

Takes an xpath expression and a file path.
Returns a list of elements matched by the expression.

### Running the test suite locally

Prerequisites:

* Python 3.14 (declared as `requires-python = ">=3.14,<4.0"` in `test/pyproject.toml`)
* Poetry 2.5.x (dependency management for python) — `poetry.lock` is
  `lock-version` 2.1 and Poetry 1.x cannot read it

In the `test/` directory, install dependencies:

```shell
poetry install
```

Run all tests:

```shell
poetry run pytest
```

Run a specific test file (paths are relative to `test/`):

```shell
poetry run pytest test_nestle1904_lowfat.py
```

Run the tests with console output:

```shell
poetry run pytest -rP
```

### Upgrading an existing checkout

`.venv` is gitignored, so pulling a branch that changes the Python version does
not replace an environment built against the old one. Poetry may also still
hold an environment it created earlier under its own cache directory, and it
prefers that over creating a new one. The result is a confusing failure that
names an interpreter you never chose and does not say where it came from:

```
Current Python version (3.13.3) is not allowed by the project (>=3.14,<4.0).
Please change python executable via the "env use" command.
```

Following that advice does not help, because `poetry env use` fails the same
way. The cached environment has to go first. Note that `poetry env remove --all`
can report nothing and delete nothing here, so check the cache directory
yourself:

```shell
poetry config cache-dir                    # e.g. ~/Library/Caches/pypoetry
ls "$(poetry config cache-dir)/virtualenvs"
```

Delete the entries whose prefix matches this project, then recreate:

```shell
rm -rf .venv
rm -rf "$(poetry config cache-dir)/virtualenvs/<project>-<hash>-py3.13"
poetry env use python3.14
poetry install
```

Repeat in each of `test/`, `pipelines/lowfat-transform/`,
`pipelines/tei-transform/` and `pipelines/tsv-transform/` — each keeps its own
environment.

To confirm which interpreter you ended up on:

```shell
poetry run python --version
```
