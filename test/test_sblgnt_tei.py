import pytest
import os
import codecs
import re
from lxml import etree
from test import __sblgnt_tei_files__, run_xpath_for_file


@pytest.mark.parametrize("tei_file", __sblgnt_tei_files__)
def test_file_exists(tei_file):
    size = os.path.getsize(tei_file)
    assert size > 0


@pytest.mark.parametrize("tei_file", __sblgnt_tei_files__)
def test_file_is_valid_utf8(tei_file):
    lines = codecs.open(tei_file, encoding="utf-8", errors="strict").readlines()
    assert lines != ""


@pytest.mark.parametrize("tei_file", __sblgnt_tei_files__)
def test_file_is_valid_xml(tei_file):
    assert etree.parse(tei_file)


@pytest.mark.parametrize("tei_file", __sblgnt_tei_files__)
def test_ref_attr_correct_format(tei_file):
    pattern = "^[A-Z0-9]{3} [0-9]+:[0-9]+![0-9]+$"  # USFM Ref
    nodes = run_xpath_for_file("//w", tei_file)
    for node in nodes:
        assert node.attrib["ref"] != ""
        assert re.match(pattern, node.attrib["ref"])


def test_number_of_words():
    total_count = 0
    for tei_file in __sblgnt_tei_files__:
        count = run_xpath_for_file("//w", tei_file)
        total_count += len(count)
    # NOTE: This assumes that we have the same number of w elements
    # as we have in the TSVs
    assert total_count == 137741
