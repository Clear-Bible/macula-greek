import os
import codecs
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
