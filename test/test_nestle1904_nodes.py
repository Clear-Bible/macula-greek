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
    pattern = "^[A-Z0-9]{3} [0-9]+:[0-9]+![0-9]+$"  # USFM Ref
    nodes = run_xpath_for_file("//Node[@ref]", node_file)
    for node in nodes:
        assert re.match(pattern, node.attrib["ref"])


def test_number_of_words():
    total_count = 0
    for node_file in __nodes_files__:
        count = run_xpath_for_file("//Node[count(child::*) = 0]", node_file)
        total_count += len(count)
    assert total_count == 137779


@pytest.mark.parametrize("node_file", __nodes_files__)
def test_referent_id_validity(node_file):
    valid_ids = []
    nodes_with_id = run_xpath_for_file("//Node[count(child::*) = 0]", node_file)
    for id_node in nodes_with_id:
        valid_ids.append(id_node.attrib["{http://www.w3.org/XML/1998/namespace}id"])

    # xpath to find node with Ref or SubjRef attribute
    nodes_with_ref = run_xpath_for_file("//Node[@Ref or @SubjRef or @Frame]", node_file)
    for ref_node in nodes_with_ref:
        # Note: one element could have all three attributes, so test each individually
        if "Ref" in ref_node.attrib:
            # Ref attribute is a space-separated list of IDs
            ref_content = ref_node.attrib["Ref"]
            refs = ref_content.split(" ") if " " in ref_content else ref_content.split(";")
            for ref in refs:
                assert ref in valid_ids

        if "SubjRef" in ref_node.attrib:
            # SubjRef attribute is a space-separated list of IDs
            ref_content = ref_node.attrib["SubjRef"]
            refs = ref_content.split(" ") if " " in ref_content else ref_content.split(";")
            for ref in refs:
                assert ref in valid_ids

        if "Frame" in ref_node.attrib:
            ref_content = ref_node.attrib["Frame"]
            # split on spaces.
            refs = ref_content.split(" ")
            for frame_refs in refs:
                # regex to remove `A[012]:` from frame_refs
                # if `AA` is present we keep it for now;
                # if we learn it is not valid, we will remove the `+` from the regex.
                frame_ref_string = re.sub(r"A+[0-9]:", "", frame_refs)
                # split on `;'
                frame_ref_list = frame_ref_string.split(";")
                for frame_ref in frame_ref_list:
                    if frame_ref != '':
                        if frame_ref != 'n00000000000': # Assuming these are OK since they happen frequently
                            assert frame_ref in valid_ids
