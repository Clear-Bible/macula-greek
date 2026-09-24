from lxml import etree
import csv

desired_filenames = [
    "01-matthew.xml",
    "02-mark.xml",
    "03-luke.xml",
    "04-john.xml",
    "05-acts.xml",
    "06-romans.xml",
    "07-1corinthians.xml",
    "08-2corinthians.xml",
    "09-galatians.xml",
    "10-ephesians.xml",
    "11-philippians.xml",
    "12-colossians.xml",
    "13-1thessalonians.xml",
    "14-2thessalonians.xml",
    "15-1timothy.xml",
    "16-2timothy.xml",
    "17-titus.xml",
    "18-philemon.xml",
    "19-hebrews.xml",
    "20-james.xml",
    "21-1peter.xml",
    "22-2peter.xml",
    "23-1john.xml",
    "24-2john.xml",
    "25-3john.xml",
    "26-jude.xml",
    "27-revelation.xml",
]

lowfat_path = "../Nestle1904/lowfat/"
__lowfat_files__ = list(map(lambda x: lowfat_path + x, desired_filenames))

nodes_path = "../Nestle1904/nodes/"
__nodes_files__ = list(map(lambda x: nodes_path + x, desired_filenames))

tei_path = "../Nestle1904/tei/"
__tei_files__ = list(map(lambda x: tei_path + x, desired_filenames))

sblgnt_lowfat_path = "../SBLGNT/lowfat/"
__sblgnt_lowfat_files__ = list(map(lambda x: sblgnt_lowfat_path + x, desired_filenames))

sblgnt_tei_path = "../SBLGNT/tei/"
__sblgnt_tei_files__ = list(map(lambda x: sblgnt_tei_path + x, desired_filenames))

nestle1904_tsv_path = "../Nestle1904/tsv/macula-greek-Nestle1904.tsv"
sblgnt_tsv_path = "../SBLGNT/tsv/macula-greek-SBLGNT.tsv"
__tsv_files__ = [nestle1904_tsv_path, sblgnt_tsv_path]

ERROR_EXPRESSION = "//*[starts-with(local-name(), 'error') or starts-with(local-name(), 'error_')]"


def read_tsv_rows(path):
    with open(path, encoding='utf-8') as file:
        return list(csv.DictReader(file, delimiter="\t"))


# Keyed by file: ids do not cross corpora, so each TSV must be validated
# against its own row set rather than a merged one.
__macula_greek_tsv_rows__ = {path: read_tsv_rows(path) for path in __tsv_files__}

def run_xpath_for_file(xpath, file):
    tree = etree.parse(file)
    return tree.xpath(xpath)
