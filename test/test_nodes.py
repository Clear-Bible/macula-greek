import pytest
import os
import codecs
from lxml import etree
from test import __nodes_files__


@pytest.mark.parametrize("nodes_file", __nodes_files__)
def test_file_exists(nodes_file):
    size = os.path.getsize(nodes_file)
    assert size > 0


@pytest.mark.parametrize("nodes_file", __nodes_files__)
def test_file_is_valid_utf8(nodes_file):
    lines = codecs.open(nodes_file, encoding="utf-8", errors="strict").readlines()
    assert lines != ""


@pytest.mark.parametrize("nodes_file", __nodes_files__)
def test_file_is_valid_xml(nodes_file):
    assert etree.parse(nodes_file)
