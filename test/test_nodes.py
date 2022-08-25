import pytest
import os
import codecs
from lxml import etree
from test import __nodes_files__, run_xpath_for_file

def all_node_elements(node_files):
    all_node_elements = []
    for node_file in node_files:
        tree = etree.parse(node_file)
        nodes = tree.xpath("//Node")
        all_node_elements += nodes
    return all_node_elements


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
    required_attrs = ["Cat", "nodeId", "morphId"]
    nodes = run_xpath_for_file("//Node", node_file)
    for node in nodes:
        for attr in required_attrs:
            assert attr in node.attrib
