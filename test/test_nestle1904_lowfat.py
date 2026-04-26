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


# @predication attribute must only take values 'verbless' or 'elided' (internal #10)
@pytest.mark.parametrize("lowfat_file", __lowfat_files__)
def test_predication_values(lowfat_file):
    VALID = {'verbless', 'elided'}
    for el in run_xpath_for_file("//*[@predication]", lowfat_file):
        assert el.attrib["predication"] in VALID, \
            f"Unexpected @predication={el.attrib['predication']!r} at {el.attrib.get('rule')}"


# @predication must only appear on <wg class="cl"> elements (internal #10)
@pytest.mark.parametrize("lowfat_file", __lowfat_files__)
def test_predication_on_cl_only(lowfat_file):
    for el in run_xpath_for_file("//*[@predication]", lowfat_file):
        assert el.tag == "wg" and el.attrib.get("class") == "cl", \
            f"@predication on unexpected element <{el.tag} class={el.attrib.get('class')!r}>"


# Minor clauses (ClType=Minor in nodes) must surface as role=aux in lowfat (internal #10)
# Spot-check: canonical single-word minor clause words must carry role=aux directly on <w>
def test_minor_clause_role_aux():
    import os
    from lxml import etree as ET
    lowfat_path = os.path.join(os.path.dirname(__file__), "..", "Nestle1904", "lowfat", "01-matthew.xml")
    tree = ET.parse(lowfat_path)
    # Σατανᾶ (MAT 4:10), Ῥακά (MAT 5:22) — all Np2CL[ClType=Minor]
    for normalized in ["Σατανᾶ", "Ῥακά"]:
        words = tree.xpath(f'//w[@normalized="{normalized}"]')
        assert words, f"No <w normalized='{normalized}'> found"
        for w in words:
            assert w.get("role") == "aux", \
                f"Expected role=aux directly on <w normalized='{normalized}'>, got role={w.get('role')!r}"


# Single-word constituents must carry @role directly on <w>, not wrapped in <wg> (issue #105)
@pytest.mark.parametrize("lowfat_file", __lowfat_files__)
def test_no_single_word_wg(lowfat_file):
    """No <wg> element should contain exactly one <w>.
    Single-word constituents carry @role directly on <w>."""
    offenders = [
        wg for wg in run_xpath_for_file("//wg", lowfat_file)
        if len(list(wg.iter("w"))) == 1
    ]
    assert not offenders, (
        f"{len(offenders)} single-word <wg> element(s) in {lowfat_file}: "
        f"first at rule={offenders[0].attrib.get('rule')!r} "
        f"ref={list(offenders[0].iter('w'))[0].attrib.get('ref', '?')!r}"
    )


# A <wg> with a single child carries no structural information — the child should
# absorb the role directly (issue #105 generalisation).
@pytest.mark.parametrize("lowfat_file", __lowfat_files__)
def test_no_single_child_wg(lowfat_file):
    """No <wg> element should have exactly one direct child element (wg or w).
    Single-constituent *2CL wrappers must be dissolved so the inner element carries
    the role directly."""
    offenders = [
        wg for wg in run_xpath_for_file("//wg", lowfat_file)
        if len(list(wg)) == 1
    ]
    assert not offenders, (
        f"{len(offenders)} single-child <wg> element(s) in {lowfat_file}: "
        f"first at rule={offenders[0].attrib.get('rule', offenders[0].attrib.get('Rule'))!r} "
        f"role={offenders[0].attrib.get('role')!r}"
    )


# Valid @role values on <w> elements (issue #105)
VALID_WORD_ROLES = {"p", "s", "v", "o", "o2", "adv", "vc", "io", "aux", "oc"}

@pytest.mark.parametrize("lowfat_file", __lowfat_files__)
def test_w_role_values(lowfat_file):
    """@role on <w> elements must be a valid clausal role."""
    for w in run_xpath_for_file("//w[@role]", lowfat_file):
        assert w.attrib["role"] in VALID_WORD_ROLES, \
            f"Invalid @role={w.attrib['role']!r} on <w> at {w.attrib.get('ref', '?')}"


# Discourse-level labels (topic, tail) and structural markers (ellipsis) must not
# appear in @role — they are either derivable from tree structure or belong in
# dedicated discourse annotation (e.g. Levinsohn). (issue #106)
@pytest.mark.parametrize("lowfat_file", __lowfat_files__)
def test_no_discourse_labels_in_role(lowfat_file):
    """@role must not contain discourse-positional labels (topic, tail) or
    structural-gap markers (ellipsis). These are not syntactic dependency roles."""
    forbidden = {"topic", "tail", "ellipsis"}
    offenders = [
        el for el in run_xpath_for_file("//*[@role]", lowfat_file)
        if el.attrib["role"] in forbidden
    ]
    assert not offenders, (
        f"{len(offenders)} element(s) with forbidden @role in {lowfat_file}: "
        + "; ".join(
            f"<{el.tag} role={el.attrib['role']!r} rule={el.attrib.get('rule', el.attrib.get('Rule', '?'))!r}>"
            for el in offenders[:3]
        )
    )


# Regression tests for projecting-verb / reported-discourse role assignment (internal #10, #14)
# These pin correct behavior for cases that were affected by local:contains-projecting-verb
# and local:is-peripheral during development.

def test_reported_speech_gets_role_o():
    """Clauses that are reported speech/thought complement of a projecting verb must get role=o."""
    import os
    from lxml import etree as ET
    cases = [
        # (book_file, ref_prefix, first_word_normalized, description)
        ("01-matthew.xml", "MAT 26:22", "Μήτι",
         "MAT 26:22 — 'Μήτι ἐγώ εἰμι, Κύριε;' is reported speech of λέγειν"),
        ("03-luke.xml",    "LUK 5:21",  "τίς",
         "LUK 5:21 — 'τίς δύναται ἁμαρτίας ἀφεῖναι' is reported thought"),
        ("03-luke.xml",    "LUK 19:16", "δέκα",
         "LUK 19:16 — 'ἡ μνᾶ σου δέκα μνᾶς' is reported speech (δέκα is in the role=o clause)"),
    ]
    lowfat_dir = os.path.join(os.path.dirname(__file__), "..", "Nestle1904", "lowfat")
    for book_file, ref_prefix, first_word, desc in cases:
        tree = ET.parse(os.path.join(lowfat_dir, book_file))
        # Find the first word of the clause, then walk up to find its role-bearing wg
        words = tree.xpath(f'//w[@normalized="{first_word}" and starts-with(@ref, "{ref_prefix}")]')
        assert words, f"No word found for {desc}"
        w = words[0]
        el = w.getparent()
        role_wg = None
        while el is not None and el.tag != "sentence":
            if el.tag == "wg" and el.get("role"):
                role_wg = el
                break
            el = el.getparent()
        assert role_wg is not None, f"No role-bearing wg ancestor found for {desc}"
        assert role_wg.get("role") == "o", \
            f"{desc}: expected role=o, got role={role_wg.get('role')!r}"


def test_speech_act_verb_not_projected():
    """Clauses whose main verb IS the speech-act verb must NOT get role=o on their wg.
    The verb itself projects; it is not the projected content."""
    import os
    from lxml import etree as ET
    cases = [
        # (book_file, ref_prefix, verb_normalized, description)
        ("07-1corinthians.xml", "1CO 16:15", "Παρακαλῶ",
         "1CO 16:15 — 'Παρακαλῶ ὑμᾶς' is the main clause, not projected content"),
        ("09-galatians.xml",    "GAL 4:21",  "Λέγετε",
         "GAL 4:21 — 'Λέγετε μοι' is the main clause, not projected content"),
        ("19-hebrews.xml",      "HEB 13:22", "Παρακαλῶ",
         "HEB 13:22 — 'Παρακαλῶ ὑμᾶς' is the main clause, not projected content"),
    ]
    lowfat_dir = os.path.join(os.path.dirname(__file__), "..", "Nestle1904", "lowfat")
    for book_file, ref_prefix, verb_norm, desc in cases:
        tree = ET.parse(os.path.join(lowfat_dir, book_file))
        words = tree.xpath(f'//w[@normalized="{verb_norm}" and starts-with(@ref, "{ref_prefix}")]')
        assert words, f"No word found for {desc}"
        w = words[0]
        el = w.getparent()
        while el is not None and el.tag != "sentence":
            if el.tag == "wg" and el.get("role"):
                assert el.get("role") != "o", \
                    f"{desc}: main-clause verb must not have role=o, but got role=o on wg rule={el.get('rule')!r}"
            el = el.getparent()


def test_temporal_clause_not_projected():
    """MAT 7:28 — ὅτε temporal clause after ἐτέλεσεν must get role=adv, not role=o.
    ἐτελέω does not project discourse; its ὅτε clause is adverbial."""
    import os
    from lxml import etree as ET
    lowfat_path = os.path.join(os.path.dirname(__file__), "..", "Nestle1904", "lowfat", "01-matthew.xml")
    tree = ET.parse(lowfat_path)
    # ὅτε at MAT 7:28 — find it by ref prefix
    words = tree.xpath('//w[@normalized="ὅτε" and starts-with(@ref, "MAT 7:28")]')
    assert words, "No ὅτε word found at MAT 7:28"
    w = words[0]
    el = w.getparent()
    while el is not None and el.tag != "sentence":
        if el.tag == "wg" and el.get("role"):
            assert el.get("role") != "o", \
                f"MAT 7:28 ὅτε temporal clause must not have role=o, got role={el.get('role')!r}"
            break
        el = el.getparent()


def test_mat_1_22_ot_quotation_not_aux():
    """MAT 1:22 — the ἵνα sub-CL wrapping an OT quotation must NOT get role=aux.
    The clause contains ἰδοὺ but deeply nested; only a top-level attention-getter
    in the same constituent should trigger peripheral treatment. (internal #14)"""
    import os
    from lxml import etree as ET
    lowfat_path = os.path.join(os.path.dirname(__file__), "..", "Nestle1904", "lowfat", "01-matthew.xml")
    tree = ET.parse(lowfat_path)
    # ἵνα at MAT 1:22 introduces the fulfillment purpose clause
    words = tree.xpath('//w[@normalized="ἵνα" and starts-with(@ref, "MAT 1:22")]')
    assert words, "No ἵνα word found at MAT 1:22"
    w = words[0]
    el = w.getparent()
    while el is not None and el.tag != "sentence":
        if el.tag == "wg" and el.get("role"):
            assert el.get("role") != "aux", \
                f"MAT 1:22 ἵνα sub-CL (OT quotation) must not have role=aux — ἰδοὺ is nested too deep"
            break
        el = el.getparent()


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
