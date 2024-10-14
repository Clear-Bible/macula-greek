import pytest
import os
import codecs
import re
from lxml import etree
from test import ERROR_EXPRESSION, __lowfat_files__, run_xpath_for_file


@pytest.mark.parametrize("lowfat_file", __lowfat_files__)
def test_file_exists(lowfat_file):
    size = os.path.getsize(lowfat_file)
    assert size > 0


@pytest.mark.parametrize("lowfat_file", __lowfat_files__)
def test_file_is_valid_utf8(lowfat_file):
    lines = codecs.open(lowfat_file, encoding="utf-8", errors="strict").readlines()
    assert lines != ""


# This includes checking the format and uniqueness of @xml:id
# `etree.parse` throws errors is the xml is not valid.
@pytest.mark.parametrize("lowfat_file", __lowfat_files__)
def test_file_is_valid_xml(lowfat_file):
    assert etree.parse(lowfat_file)


@pytest.mark.parametrize("lowfat_file", __lowfat_files__)
def test_ref_attr_correct_format(lowfat_file):
    pattern = "^[A-Z0-9]{3} [0-9]+:[0-9]+![0-9]+$"  # USFM Ref
    nodes = run_xpath_for_file("//w", lowfat_file)
    for node in nodes:
        assert node.attrib["ref"] != ""
        assert re.match(pattern, node.attrib["ref"])


@pytest.mark.parametrize("lowfat_file", __lowfat_files__)
def test_required_attrs_exist_on_w_elements(lowfat_file):
    required_attrs = [
        "ref",
        "after",
        "class",
        "{http://www.w3.org/XML/1998/namespace}id",  # @xml:id
        "lemma",
        "normalized",
        "strong",
        "gloss",
        # "domain", # not present everywhere
        # "ln", # not present everywhere
        "morph",
        "unicode",
    ]
    nodes = run_xpath_for_file("//w", lowfat_file)
    for node in nodes:
        for attr in required_attrs:
            assert attr in node.attrib


# Unable to determine required attrs for `wg` at this time.
# @pytest.mark.parametrize("lowfat_file", __lowfat_files__)
# def test_required_attrs_exist_on_wg_elements(lowfat_file):
#     required_attrs = [ "class" ]
#     nodes = run_xpath_for_file("//wg", lowfat_file)
#     for node in nodes:
#         for attr in required_attrs:
#             assert attr in node.attrib


def test_number_of_words():
    total_count = 0
    for lowfat_file in __lowfat_files__:
        count = run_xpath_for_file("//w", lowfat_file)
        total_count += len(count)
    assert total_count == 137779


# Expected failure.
# See: https://github.com/Clear-Bible/macula-greek/issues/92#issuecomment-2407973591
@pytest.mark.xfail
@pytest.mark.parametrize("lowfat_file", __lowfat_files__)
def test_no_errors(lowfat_file):
    count = len(run_xpath_for_file(ERROR_EXPRESSION, lowfat_file))
    assert count == 0


@pytest.mark.parametrize("lowfat_file", __lowfat_files__)
def test_referent_id_validity(lowfat_file):
    valid_ids = []
    nodes_with_id = run_xpath_for_file("//w", lowfat_file)
    for id_node in nodes_with_id:
        valid_ids.append(id_node.attrib["{http://www.w3.org/XML/1998/namespace}id"])

    # xpath to find node with Ref or SubjRef attribute
    nodes_with_ref = run_xpath_for_file("//w[@referent or @subjref or @frame]", lowfat_file)
    for ref_node in nodes_with_ref:
        # Note: one element could have all three attributes, so test each individually
        if "referent" in ref_node.attrib:
            # Ref attribute is a space-separated list of IDs
            ref_content = ref_node.attrib["referent"]
            refs = ref_content.split(" ") if " " in ref_content else ref_content.split(";")
            for ref in refs:
                assert ref in valid_ids

        if "subjref" in ref_node.attrib:
            # SubjRef attribute is a space-separated list of IDs
            ref_content = ref_node.attrib["subjref"]
            refs = ref_content.split(" ") if " " in ref_content else ref_content.split(";")
            for ref in refs:
                assert ref in valid_ids

        if "Frame" in ref_node.attrib:
            ref_content = ref_node.attrib["frame"]
            # split on spaces.
            refs = ref_content.split(" ")
            for frame_refs in refs:
                # regex to remove `A[012]:` from frame_refs
                # Actually, `AA:`, `A0:`, `A1:`, `A2:`, and `AA2:` are valid.
                # (but `AA:` only in Hebrew at present)
                frame_ref_string = re.sub(r"A+[0-2]{0,1}:", "", frame_refs)
                # split on `;'
                frame_ref_list = frame_ref_string.split(";")
                for frame_ref in frame_ref_list:
                    if frame_ref != '':
                        if frame_ref != 'n00000000000': # Assuming these are OK since they happen frequently
                            assert frame_ref in valid_ids
