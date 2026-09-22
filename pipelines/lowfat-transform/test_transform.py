# Tests for the nodes -> lowfat transform.
#
# These run against the committed corpus rather than fixtures: the pipeline's
# contract is that a clean run reproduces the tracked output byte for byte, and
# the tracked output is the only thing that can prove it.

import xml.etree.ElementTree as ElementTree

import pytest

import main

EDITIONS = ["Nestle1904", "SBLGNT"]

# The deepest tree in either corpus. The Luke 3:23-38 genealogy is a recursive
# NP-of-NP chain -- every "son of X" wraps the whole phrase that precedes it --
# so it nests far deeper than ordinary prose, which peaks around 25.
DEEPEST_BOOK = "03-luke.xml"

# JDK 25, which SaxonC 13 is built on, defaults jdk.xml.maxElementDepth to 100
# and aborts the parse beyond it. SaxonC 12 was built on a JDK that did not.
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


@pytest.mark.parametrize("edition", EDITIONS)
def test_deepest_book_exceeds_the_jdk_element_depth_limit(edition):
    # Guards the guard: if the corpus ever stops nesting past the JDK limit,
    # the workaround in main.py is no longer load-bearing and the transform
    # test below silently stops covering it. Fail loudly instead.
    source = main.REPO_ROOT / edition / "nodes" / DEEPEST_BOOK
    assert max_element_depth(source) > JDK_ELEMENT_DEPTH_LIMIT


@pytest.mark.parametrize("edition", EDITIONS)
def test_deepest_book_transforms_to_the_committed_lowfat(edition, tmp_path):
    source = main.REPO_ROOT / edition / "nodes" / DEEPEST_BOOK
    dest = tmp_path / DEEPEST_BOOK

    main.transform(source, dest)
    main.reformat(dest)

    committed = main.REPO_ROOT / edition / "lowfat" / DEEPEST_BOOK
    assert dest.read_text() == committed.read_text()
