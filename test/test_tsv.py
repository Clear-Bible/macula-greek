import os
import codecs
import re
import pytest
from test import __macula_greek_tsv_rows__, __tsv_files__

NODE_COUNT = 137779

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
def test_tsv_row_has_id():
    for tsv_row in __macula_greek_tsv_rows__:
        id = tsv_row["xml:id"]
        assert id != ""
        assert id[0] == "n"

# Verify the correct number of nodes.
def test_tsv_row_count():
    total_count = len(__macula_greek_tsv_rows__)
    assert total_count == NODE_COUNT


def test_tsv_row_has_valid_referent_ids():
    valid_ids = set()
    for tsv_row in __macula_greek_tsv_rows__:
        id = tsv_row["xml:id"]
        valid_ids.add(id)

    # Verify that each referent id is valid.
    for tsv_row in __macula_greek_tsv_rows__:
        # test referent
        referent_id = tsv_row["referent"]
        if referent_id != "":
            referents = referent_id.split(" ")
            for referent in referents:
                assert referent in valid_ids

        # test subjref
        subjref_id = tsv_row["subjref"]
        if subjref_id != "":
            # subjref apparently delimit with either space or semicolon
            subjrefs = subjref_id.split(" ") if " " in subjref_id else subjref_id.split(";")
            # subjrefs = subjref_id.split(";")
            for subjref in subjrefs:
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
                        if frame_ref != 'n00000000000': # Assuming these are OK since they happen frequently
                            assert frame_ref in valid_ids
