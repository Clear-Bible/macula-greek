# lowfat-transform pipeline

This pipeline transforms the `nodes` trees into `lowfat` by running
`mappings/lowfat-macula-greek.xquery` through SaxonC-HE (the `saxonche` Python
package), then applies a small post-processing pass.

Note that this is an **XQuery** transform, not XSLT — unlike the sibling
[tei-transform](../tei-transform) pipeline. Saxon writes the XML declaration,
the two `<?xml-stylesheet?>` processing instructions and the indentation
(`declare option output:indent 'yes'` in the XQuery), so the `reformat()` pass
in `main.py` only adds a trailing space after each `</milestone>` and drops
Saxon's final newline.

## Requirements

- **Python 3.14.** Declared as `requires-python = ">=3.14,<4.0"` in
  `pyproject.toml` and pinned in CI. The real constraint is wheel availability:
  `saxonche` ships no sdist at all, so a release without a wheel for your
  interpreter fails outright with `Unable to find installation candidates for
  saxonche`. 13.0.0 publishes cp39–cp314 wheels (including cp314t, the
  free-threaded build) for macOS (x86_64 and arm64), manylinux (x86_64 and
  aarch64) and Windows.
- **Poetry 2.5.x.** CI pins 2.5.1 in `.github/workflows/pr.yml`. `poetry.lock`
  is `lock-version` 2.1, which Poetry 1.x cannot read.

## Upgrading an existing checkout

If `poetry install` fails with `Current Python version (…) is not allowed by the
project`, a virtualenv built against an older Python is still in the way. See
[UNIT-TEST.md](../../UNIT-TEST.md#upgrading-an-existing-checkout) for how to
clear it.

## Usage

```shell
cd pipelines/lowfat-transform
poetry install
poetry run python main.py Nestle1904
poetry run python main.py SBLGNT
```

`poetry shell` was removed in Poetry 2.0. Either prefix each command with
`poetry run` as above, or activate the environment once with
`poetry env activate`.

Each edition takes roughly five seconds with ten workers on fourteen cores.

## What it reads and writes

For edition `<E>` (`Nestle1904` or `SBLGNT`):

- reads `<E>/nodes/*.xml` — 27 per-book files
- **overwrites `<E>/lowfat/<same filename>` in place**

Those outputs are tracked files, so review the result with `git diff` before
committing. A clean run against unchanged inputs reproduces the committed
output byte for byte, which means `git status` should come back empty; anything
else is a real change worth inspecting.

The stylesheets (`*.css`) and the XInclude index files
(`SBLGNT/lowfat/sblgntlowfat.xml`, `Nestle1904/lowfat/nestle1904lowfat.xml`,
`Nestle1904/lowfat/commonformat.xml`) are not regenerated — only the 27
per-book files are.

## Element depth

SaxonC 13 is built with GraalVM Native Image 25, so it inherits the JDK 25
default of `jdk.xml.maxElementDepth=100`. SaxonC 12 did not. The Luke 3:23-38
genealogy is a recursive NP-of-NP chain — each "son of X" wraps the whole
phrase before it — nesting about 160 levels, so under that cap `03-luke.xml`
aborts in both editions:

```
SXXP0003 Error reported by XML parser: JAXP00010006: The element "Node" has a
depth of "101" that exceeds the limit "100" set by "jdk.xml.maxElementDepth".
```

`transform()` lifts the cap by setting Saxon's `parserProperty` feature URI for
`maxElementDepth` to `0`. This is why the version floor is `13.0.0` rather than
13 merely happening to work. `test_transform.py` pins the behaviour, and also
asserts the corpus still nests past 100 so the workaround cannot quietly stop
being load-bearing.

The sibling [tsv-transform](../tsv-transform) pipeline carries the same
property for the same reason; so did the `mappings/generate-tsv.sh` it replaced,
as `BASEX_JVM=-Djdk.xml.maxElementDepth=0`.

## Tests

```shell
poetry run pytest
```

The tests transform the deepest book in each edition and compare the result
against the committed `lowfat` output, so they need the corpus present but
write only to a temporary directory.

## Tuning

`MAX_WORKERS` sets the process-pool size and defaults to `cpu_count() - 1`. On
a single-CPU machine that default evaluates to `0` and the run fails with
`ValueError: max_workers must be greater than 0`, so set it explicitly there:

```shell
MAX_WORKERS=1 poetry run python main.py SBLGNT
```

## Debugging

`SERIAL=1` skips the process pool and transforms the books one at a time in the
current process:

```shell
SERIAL=1 poetry run python main.py SBLGNT
```

Use this when a book fails. In the default parallel path the work happens in a
worker process, so the traceback bottoms out in `concurrent.futures` plumbing
and a debugger cannot attach. Serially the traceback runs all the way down
through `do_transform` and `transform` to the failing Saxon call, the run stops
at the first bad file instead of processing the rest first, and `pdb`/`ipdb`
work normally.

Note that `SERIAL=1` is not the same as `MAX_WORKERS=1`: the latter still uses a
worker process.
