import os
import codecs
import re
import pytest
from test import __macula_greek_tsv_rows__, __tsv_files__

# Expected data row count per TSV, which must equal count(//w) over the
# corresponding lowfat XML. Regenerate both with `./mappings/generate-tsv.sh all`.
NODE_COUNTS = {
    "../Nestle1904/tsv/macula-greek-Nestle1904.tsv": 137779,
    "../SBLGNT/tsv/macula-greek-SBLGNT.tsv": 137741,
}

# Null sentinel used by the annotation for a reference that was never resolved
# to a word, e.g. the unresolved antecedent of the pronouns in MRK 10:3-5.
# It appears in `frame`, `referent`, and `subjref`, and is not a dangling id.
UNRESOLVED_ID = "n00000000000"

# A Louw-Nida sense is a domain and sense number with an optional subsense
# letter (`93.169a`), space separated when a word carries more than one.
# The MARBLE extraction has emitted senses with a trailing source annotation
# instead, e.g. `12.9{N:001}` for MAT 1:20!7, which is not a usable LN value.
LN_EXPRESSION = re.compile(r"^\d+\.\d+[a-z]?( \d+\.\d+[a-z]?)*$")

# Verify that the file exists.
@pytest.mark.parametrize("tsv_file", __tsv_files__)
def test_files_exists(tsv_file):
    size = os.path.getsize(tsv_file)
    assert size > 0

# Verify that the file is in utf8 format.
@pytest.mark.parametrize("tsv_file", __tsv_files__)
def test_file_is_valid_utf8(tsv_file):
    lines = codecs.open(tsv_file, encoding="utf-8", errors="strict").readlines()
    assert lines != ""

# Verify a node id that is correctly formatted in each row.
@pytest.mark.parametrize("tsv_file", __tsv_files__)
def test_tsv_row_has_id(tsv_file):
    for tsv_row in __macula_greek_tsv_rows__[tsv_file]:
        id = tsv_row["xml:id"]
        assert id != ""
        assert id[0] == "n"

# Verify the correct number of nodes.
@pytest.mark.parametrize("tsv_file", __tsv_files__)
def test_tsv_row_count(tsv_file):
    total_count = len(__macula_greek_tsv_rows__[tsv_file])
    assert total_count == NODE_COUNTS[tsv_file]


# Verify that every Louw-Nida sense is well formed.
@pytest.mark.parametrize("tsv_file", __tsv_files__)
def test_tsv_row_has_well_formed_ln(tsv_file):
    for tsv_row in __macula_greek_tsv_rows__[tsv_file]:
        ln = tsv_row["ln"]
        if ln != "":
            assert LN_EXPRESSION.match(ln), (
                f"{tsv_row['xml:id']} ({tsv_row['ref']}) has malformed ln {ln!r}"
            )



@pytest.mark.parametrize("tsv_file", __tsv_files__)
def test_tsv_row_has_valid_referent_ids(tsv_file):
    tsv_rows = __macula_greek_tsv_rows__[tsv_file]

    valid_ids = set()
    for tsv_row in tsv_rows:
        id = tsv_row["xml:id"]
        valid_ids.add(id)

    # Verify that each referent id is valid.
    for tsv_row in tsv_rows:
        # test referent
        referent_id = tsv_row["referent"]
        if referent_id != "":
            referents = referent_id.split(" ")
            for referent in referents:
                if referent != UNRESOLVED_ID:
                    assert referent in valid_ids

        # test subjref
        subjref_id = tsv_row["subjref"]
        if subjref_id != "":
            # subjref apparently delimit with either space or semicolon
            subjrefs = subjref_id.split(" ") if " " in subjref_id else subjref_id.split(";")
            # subjrefs = subjref_id.split(";")
            for subjref in subjrefs:
                if subjref != UNRESOLVED_ID:
                    assert subjref in valid_ids

        # test frame
        frame_id = tsv_row["frame"]
        if frame_id != "":
            refs = frame_id.split(" ")
            for frame_refs in refs:
                # regex to remove `A[012]:` from frame_refs
                # Actually, `AA:`, `A0:`, `A1:`, `A2:`, and `AA2:` are valid.
                # (but `AA:` only in Hebrew at present)
                frame_ref_string = re.sub(r"A+[0-2]{0,1}:", "", frame_refs)
                # split on `;'
                frame_ref_list = frame_ref_string.split(";")
                for frame_ref in frame_ref_list:
                    if frame_ref != '':
                        if frame_ref != UNRESOLVED_ID:
                            assert frame_ref in valid_ids
