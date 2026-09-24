# tsv-transform pipeline

This pipeline generates the word-level TSV tables from the `lowfat` XML by
running `mappings/greek-lowfat-to-tsv.xq` through SaxonC-HE (the `saxonche`
Python package).

It replaces `mappings/generate-tsv.sh`, which drove the same query through
BaseX. BaseX was the last tool in this repository that had to be installed
separately, and the last reason to have a JVM on hand; because CI could not
install it, the TSV step was also the only transform CI could not so much as
smoke-test. The query itself is unchanged — it was never the problem.

Like [lowfat-transform](../lowfat-transform) this is an **XQuery** transform,
not XSLT. Saxon writes the file directly: `main.py` sets the serialization
method to `text` with a newline item separator, which produces the tab-separated
rows and leaves the final row unterminated, exactly as the committed files are
stored. There is no post-processing pass.

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
cd pipelines/tsv-transform
poetry install
poetry run python main.py all
```

Either edition can be run on its own:

```shell
poetry run python main.py SBLGNT
poetry run python main.py Nestle1904
```

The argument is required. Running with no argument prints the usage line and
exits non-zero rather than regenerating both, which is a cheap guard against
overwriting two tracked 20 MB files by accident.

`poetry shell` was removed in Poetry 2.0. Either prefix each command with
`poetry run` as above, or activate the environment once with
`poetry env activate`.

Each edition takes roughly eight seconds.

## What it reads and writes

For edition `<E>` (`Nestle1904` or `SBLGNT`):

- reads `<E>/lowfat/<e>lowfat.xml`, the XInclude index, which pulls in all 27
  per-book files
- **overwrites `<E>/tsv/macula-greek-<E>.tsv` in place**

Those outputs are tracked files, so review the result with `git diff` before
committing. A clean run against unchanged inputs reproduces the committed
output byte for byte, which means `git status` should come back empty; anything
else is a real change worth inspecting.

Note the ordering dependency: the TSVs are derived from the `lowfat` XML, so
regenerate `lowfat` first if both are in play. Otherwise a TSV diff cannot be
told apart from a lowfat diff.

## The two Saxon configuration properties

Both existed as BaseX flags in the script this replaced, and omitting either one
still fails quietly or confusingly. `test_transform.py` pins both.

- **XInclude** (`xi`), off by default in Saxon, was `-O xinclude=true`. The
  inputs are XInclude indexes over the 27 per-book files, not merged corpora,
  so without it `//w` matches nothing and the query writes a 173-byte file
  containing only its header row — no error, no warning.
- **Element depth**, the `parserProperty` feature URI for `maxElementDepth`,
  was `BASEX_JVM=-Djdk.xml.maxElementDepth=0`. SaxonC 13 is built with GraalVM
  Native Image 25, so it inherits the JDK 25 default cap of 100; the Luke
  3:23-38 genealogy is a recursive NP-of-NP chain nesting `<wg class="np">`
  about 160 levels deep.

  The depth failure names the wrong thing. The native image ships no XInclude
  message bundle, so it surfaces as

  ```
  Could not load any resource bundle by
  com.sun.org.apache.xerces.internal.impl.msg.XIncludeMessages
  ```

  and the real error is visible only on stderr:

  ```
  SXXP0003 Error reported by XML parser: JAXP00010006: The element "w" has a
  depth of "101" that exceeds the limit "100" set by "jdk.xml.maxElementDepth".
  ```

  If you ever see that resource-bundle message, the element depth cap is what
  to look at.

## If regeneration comes back short

`main.py` exits non-zero if a result holds fewer than `MINIMUM_ROWS` (100,000)
data rows, which is the backstop for the silent header-only failure above. Both
corpora hold about 137,700 rows, so the threshold has plenty of headroom for a
real data change.

The guard reports; it cannot prevent. The output file has already been
overwritten by the time the count is taken, so recover with:

```shell
git checkout -- SBLGNT/tsv/macula-greek-SBLGNT.tsv
```

## Tests

```shell
poetry run pytest
```

The tests transform both editions and compare the result against the committed
TSVs byte for byte, so they need the corpus present but write only to a
temporary directory. They take about twenty seconds.

## Why there is no process pool

The sibling pipelines spread 27 per-book files across a `ProcessPoolExecutor`
and expose `MAX_WORKERS` and `SERIAL`. This one runs serially and exposes
neither, deliberately.

There are only two units of work here, and only `all` has more than one, so the
best case is about eight seconds saved, once — against which each worker pays
process spawn plus a fresh initialization of the SaxonC native image, and two
concurrent processors mean two fully expanded 27-book corpora resident at the
same time. `SERIAL=1` exists in the siblings solely to escape the pool for
debugging; with no pool there is nothing to escape, tracebacks already run down
to the failing Saxon call, and `pdb`/`ipdb` already work.
