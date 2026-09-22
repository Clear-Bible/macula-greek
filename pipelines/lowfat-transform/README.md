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
  saxonche`. 12.10.0 publishes cp39–cp314 wheels for macOS (x86_64 and arm64),
  manylinux (x86_64 and aarch64) and Windows.
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
