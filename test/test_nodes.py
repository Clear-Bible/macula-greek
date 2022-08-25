import pytest
import os
import codecs
import re
from lxml import etree
from test import __nodes_files__, run_xpath_for_file

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


@pytest.mark.parametrize("node_file", __nodes_files__)
def test_each_node_has_required_attr(node_file):
    required_attrs = ["Cat", "nodeId"]
    nodes = run_xpath_for_file("//Node", node_file)
    for node in nodes:
        for attr in required_attrs:
            assert attr in node.attrib

@pytest.mark.parametrize("node_file", __nodes_files__)
def test_ref_attr_correct_format(node_file):
    pattern = '^[A-Z0-9]{3} [0-9]+:[0-9]+![0-9]+$' # USFM Ref
    nodes = run_xpath_for_file('//Node[@ref]', node_file)
    for node in nodes:
        assert re.match(pattern, node.attrib['ref'])

