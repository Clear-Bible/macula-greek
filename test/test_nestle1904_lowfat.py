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


# Wrapper-clause rules are exempt from the @class requirement pending semantic redesign (issue #104).
# Conjuncted/group rules are exempt pending the broader @class fix (issue #103).
# All other <wg> elements must have @class or @type.
WRAPPER_CLAUSE_RULES = {
    # issue #104 — semantics of wrapper rules not yet defined
    "AdjpCL", "AdvpCL", "PtclCL", "DetCL", "sub-CL", "that-VP", "Conj-CL",
    # issue #103 — conjuncted/group structures missing @class in XQuery else-branch
    "2CLaCL", "2CLaCLaCL", "2NpaNpaNp", "2PpaPp",
    "3NpaNp", "4NpaNp",
    "ADVaADV", "AdjpaAdjp", "AdvpaAdvp", "aAdvpaAdvp",
    "CLa2CL", "CLaCL", "CLandCL2", "CLandClClandClandClandCl",
    "ClCl", "ClCl2",
    "Conj12CL", "Conj12Np", "Conj13CL", "Conj14CL",
    "Conj2Nump", "Conj2P", "Conj2Pp", "Conj2VP",
    "Conj3ADV", "Conj3Adjp", "Conj3Advp", "Conj3CL", "Conj3Np", "Conj3Pp", "Conj3VP",
    "Conj4CL", "Conj4Np", "Conj4Pp",
    "Conj5AdjP", "Conj5CL", "Conj5Np", "Conj5Pp",
    "Conj6CL", "Conj6Np", "Conj6P",
    "Conj7CL", "Conj7Np", "Conj7Pp",
    "Conj8Np", "Conj9Np", "ConjNp",
    "EitherOr10Np", "EitherOr3Vp", "EitherOr4Advp", "EitherOr4CL", "EitherOr4Np",
    "EitherOr4Pp", "EitherOr4Vp", "EitherOr5Vp", "EitherOr7CL", "EitherOr8Np",
    "EitherOrAdjp", "EitherOrVp",
    "Intj2CL", "Np2CL",
    "NpNpNpNpNpNpNpNpNpNpNpNpNpNpNpAndNp", "NpaNp",
    "aCLaCL", "aCLaCLaCL", "aNpaNp", "aNpaNpaNp", "aPpaPp", "aPpaPpaPp",
    "",  # <wg> with no rule at all
}


@pytest.mark.parametrize("lowfat_file", __lowfat_files__)
def test_required_attrs_exist_on_wg_elements(lowfat_file):
    nodes = run_xpath_for_file("//wg", lowfat_file)
    for node in nodes:
        rule = node.attrib.get("rule") or node.attrib.get("Rule", "")
        if rule in WRAPPER_CLAUSE_RULES:
            continue
        assert "class" in node.attrib or "type" in node.attrib, \
            f"<wg> missing @class/@type: rule={rule!r} nodeId={node.attrib.get('nodeId')!r}"


def test_number_of_words():
    total_count = 0
    for lowfat_file in __lowfat_files__:
        count = run_xpath_for_file("//w", lowfat_file)
        total_count += len(count)
    assert total_count == 137779


@pytest.mark.parametrize("lowfat_file", __lowfat_files__)
def test_no_errors(lowfat_file):
    count = len(run_xpath_for_file(ERROR_EXPRESSION, lowfat_file))
    assert count == 0


# Regression: @cltype debug attribute was accidentally emitted (internal #7)
@pytest.mark.parametrize("lowfat_file", __lowfat_files__)
def test_no_cltype_attr(lowfat_file):
    offenders = run_xpath_for_file("//*[@cltype]", lowfat_file)
    assert not offenders


# Regression: length heuristic was stripping final letters into @after (public #76)
@pytest.mark.parametrize("lowfat_file", __lowfat_files__)
def test_after_no_alphabetic(lowfat_file):
    XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
    for w in run_xpath_for_file("//w[@after]", lowfat_file):
        after = w.attrib["after"]
        alpha = [c for c in after if c.isalpha()]
        assert not alpha, \
            f"Alphabetic chars {alpha!r} in @after={after!r} at {w.attrib.get(XML_ID)}"


# Regression: em-dash prefix words (e.g. —νυνί) were having their final letter stripped
@pytest.mark.parametrize("lowfat_file", __lowfat_files__)
def test_em_dash_words_not_truncated(lowfat_file):
    XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
    for w in run_xpath_for_file("//w[starts-with(@unicode, '\u2014')]", lowfat_file):
        after = w.attrib.get("after", "")
        alpha = [c for c in after if c.isalpha()]
        assert not alpha, \
            f"Alphabetic chars stripped into @after for {w.attrib.get('unicode')!r}: after={after!r} at {w.attrib.get(XML_ID)}"


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
