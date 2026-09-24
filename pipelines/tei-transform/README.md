# tei-transform pipeline

This pipeline uses XSLT to transform the SBLGNT XML into something resembling
our Nestle1904 TEI. The stylesheet is `fixtures/sblgnt-tei.xsl`, applied with
`lxml`; the chapter regrouping, verse references and `xml:id` generation are
Python extension functions registered under the `urn:python-funcs` namespace,
so the stylesheet cannot be run on its own with a standalone XSLT processor.

Book metadata comes from `fixtures/bible-books-lookup.json`, which is read at
import time — `main.py` will not even import if that file is missing.

## Requirements

- **Python 3.10, 3.11 or 3.12.** Not 3.13 or later: the pinned `lxml` 4.9.3
  has no wheel for 3.13 and does not build from its sdist there.
- **Poetry 1.2.x.** CI pins 1.2.2 in `.github/workflows/pr.yml`. The
  `poetry shell` step below was removed in Poetry 2.0; on 2.x either use
  `poetry env activate`, or skip the shell and run `poetry run python main.py`.

## Usage

```shell
cd pipelines/tei-transform
poetry install
poetry shell
python main.py
```

The whole run takes about a second.

## What it reads and writes

- reads `sources/LogosBible/SBLGNT/data/sblgnt/xml/*.xml`, selecting the 27
  per-book files by name; the merged `sblgnt.xml` in that directory is skipped
- **overwrites all 27 `SBLGNT/tei/*.xml` in place**

Those outputs are tracked files, so review the result with `git diff` before
committing. A clean run against unchanged inputs reproduces the committed
output byte for byte, which means `git status` should come back empty.

There is no argument to limit the run to a single book — `main.py` takes no
command-line arguments at all.

## Tuning

`MAX_WORKERS` sets the process-pool size and defaults to `cpu_count() - 1`. On
a single-CPU machine that default evaluates to `0` and the run fails with
`ValueError: max_workers must be greater than 0`, so set it explicitly there.

## If a book fails to transform

Re-run it with `SERIAL=1`, which skips the process pool and transforms the books
one at a time in the current process:

```shell
SERIAL=1 python main.py
```

This matters here more than in most pipelines. `main.py` has `ipdb.set_trace()`
and `pdb.set_trace()` inside two exception handlers, and in the default parallel
path those handlers run inside `ProcessPoolExecutor` workers — several workers
would try to open an interactive debugger at once, so a failing run looks like a
hang rather than an error. Run serially and those debuggers behave as intended,
the traceback keeps the pipeline's own frames instead of bottoming out in
`concurrent.futures`, and the run stops at the first bad book.

If you do hit the parallel path with a failure, redirect stdin so the debugger
raises instead of hanging and the real exception surfaces:

```shell
python main.py < /dev/null
```

Note also that `ipdb` is in the `dev` dependency group, so an install that
excludes dev dependencies turns that error path into a `ModuleNotFoundError`.

`SERIAL=1` is not the same as `MAX_WORKERS=1`: the latter still uses a worker
process.
