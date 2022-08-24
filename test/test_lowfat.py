import pytest

def test_number_of_files(lowfat_files):
    assert len(lowfat_files) == 27
