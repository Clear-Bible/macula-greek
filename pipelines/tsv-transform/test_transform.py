# Tests for the lowfat -> TSV transform.
#
# Like the sibling lowfat-transform tests, these run against the committed
# corpus: the pipeline's contract is that a clean run reproduces the tracked
# TSVs byte for byte, and the tracked TSVs are the only thing that can prove it.
# Nothing here writes inside the repository.

import xml.etree.ElementTree as ElementTree

import pytest

import main

# The deepest tree in either corpus, as pulled in by the XInclude indexes the
# pipeline reads. The Luke 3:23-38 genealogy is a recursive NP-of-NP chain, so
# it nests far deeper than ordinary prose.
DEEPEST_BOOK = "03-luke.xml"

# JDK 25, which SaxonC 13 is built on, defaults jdk.xml.maxElementDepth to 100
# and aborts the parse beyond it.
JDK_ELEMENT_DEPTH_LIMIT = 100


def max_element_depth(path):
    depth = maximum = 0
    for event, _ in ElementTree.iterparse(path, events=("start", "end")):
        if event == "start":
            depth += 1
            maximum = max(maximum, depth)
        else:
            depth -= 1
    return maximum


@pytest.mark.parametrize("edition", main.EDITIONS)
def test_deepest_book_exceeds_the_jdk_element_depth_limit(edition):
    # Guards the guard: if the corpus ever stops nesting past the JDK limit,
    # the depth workaround in main.py is no longer load-bearing and the
    # transform test below silently stops covering it. Fail loudly instead.
    source, _ = main.EDITIONS[edition]
    book = main.REPO_ROOT / source.parent / DEEPEST_BOOK
    assert max_element_depth(book) > JDK_ELEMENT_DEPTH_LIMIT


@pytest.mark.parametrize("edition", main.EDITIONS)
def test_transform_reproduces_the_committed_tsv(edition, tmp_path):
    # Byte comparison rather than a parsed one: the tab separation, the absence
    # of quoting, the LF line endings and the missing final newline are all
    # part of the committed format, and a row-wise comparison would miss them.
    source, dest_name = main.EDITIONS[edition]
    dest = tmp_path / dest_name.name

    main.transform(main.REPO_ROOT / source, dest)

    assert dest.read_bytes() == (main.REPO_ROOT / dest_name).read_bytes()


def test_short_result_is_rejected(tmp_path):
    # A TSV that lost its XIncludes still parses and still has a header, so
    # only the row count catches it. See main.MINIMUM_ROWS.
    header_only = tmp_path / "header-only.tsv"
    header_only.write_text("xml:id\tref\trole\n", encoding="utf-8")

    with pytest.raises(SystemExit):
        main.check_row_count(header_only)


def test_full_result_is_accepted(tmp_path):
    full = tmp_path / "full.tsv"
    full.write_text("header\n" + "row\n" * main.MINIMUM_ROWS, encoding="utf-8")

    assert main.check_row_count(full) > main.MINIMUM_ROWS
