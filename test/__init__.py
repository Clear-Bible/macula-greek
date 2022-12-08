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

def run_xpath_for_file(xpath, file):
    tree = etree.parse(file)
    return tree.xpath(xpath)
