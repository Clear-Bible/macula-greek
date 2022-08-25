import pytest
import os
import codecs
from lxml import etree
from test import __nodes_files__


node_required_attributes = ["Cat", "nodeId", "morphId"]


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


@pytest.mark.parametrize("node", all_node_elements(__nodes_files__))
@pytest.mark.parametrize("attr", node_required_attributes)
# paramaterizing by node seems like it would be nice for reporting,
# but doing this for single test took the suite from < 5 seconds to
# > 15 minutes, using 10+ GB of memory.
# I'm thinking the test suite will err on the side of
# "finding problems quickly" rather than "exhaustive error reporting".
# The latter would need to be reserved for manual queries when trying to solve a problem.
def test_each_node_has_required_attr(node, attr):
    assert attr in node.attrib
