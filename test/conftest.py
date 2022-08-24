import pytest
import os

ignored_lowfat_files = ["commonformat.xml", "nestle1904lowfat.xml"]


def lowfat_filename_filter(filename):
    if filename.endswith("xml"):
        if filename not in ignored_lowfat_files:
            return True
        else:
            return False
    else:
        return False


@pytest.fixture
def lowfat_files():
    path_prefix = "./Nestle1904/lowfat/"
    lowfat_directory_contents = os.listdir(path_prefix)
    filtered_lowfat_directory_contents = filter(
        lowfat_filename_filter, lowfat_directory_contents
    )
    return list(map(lambda f: path_prefix + f, filtered_lowfat_directory_contents))
