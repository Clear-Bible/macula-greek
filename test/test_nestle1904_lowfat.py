import pytest
import os
import codecs
import re
from lxml import etree
from test import __lowfat_files__, run_xpath_for_file


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
