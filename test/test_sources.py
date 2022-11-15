import pytest
import os
import csv
import codecs
import re
from test import __wordsense_tsv_rows__, wordsense_tsv_path

# The two columns in the wordsense TSV.
ID_ATTR = 'macula_greek_word_id'
SENSE_ATTR = 'sense_number'

# Make sure the wordsense TSV exists.
def test_file_exists():
    size = os.path.getsize(wordsense_tsv_path)
    assert size > 0

# Make sure the wordsense TSV has the correct header attributes.
def test_ref_attr_correct_format():
    id_attr, sense_attr = __wordsense_tsv_rows__[0]
    assert id_attr == ID_ATTR
    assert sense_attr == SENSE_ATTR

# Make sure all IDs in the wordsense TSV are formatted correctly.
def test_tsv_row_has_ids():
    for tsv_row in __wordsense_tsv_rows__:
        id = tsv_row[ID_ATTR]
        assert id != ""
        assert id[0] == "n"
