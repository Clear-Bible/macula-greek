import pytest
import os
import codecs
from lxml import etree
from test import __tei_files__


@pytest.mark.parametrize("tei_file", __tei_files__)
def test_file_exists(tei_file):
    size = os.path.getsize(tei_file)
    assert size > 0


@pytest.mark.parametrize("tei_file", __tei_files__)
def test_file_is_valid_utf8(tei_file):
    lines = codecs.open(tei_file, encoding="utf-8", errors="strict").readlines()
    assert lines != ""


@pytest.mark.parametrize("tei_file", __tei_files__)
def test_file_is_valid_xml(tei_file):
    assert etree.parse(tei_file)
