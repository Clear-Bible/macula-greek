import re
import pytest
from lxml import etree
from test import __lowfat_files__, __sblgnt_lowfat_files__

XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
FRAME_PREFIX_RE = re.compile(r"A+[0-2]{0,1}:")


def _collect_valid_ids(files):
    valid = set()
    for f in files:
        tree = etree.parse(f)
        for xid in tree.xpath("//w/@*[local-name()='id']",
                               namespaces={"xml": "http://www.w3.org/XML/1998/namespace"}):
            valid.add(xid)
    return valid


def _check_referents(files, valid_ids):
    failures = []
    for f in files:
        tree = etree.parse(f)
        for w in tree.xpath("//w[@referent or @subjref or @frame]"):
            for attr in ("referent", "subjref"):
                val = w.attrib.get(attr, "")
                if not val:
                    continue
                refs = val.split(" ") if " " in val else val.split(";")
                for ref in refs:
                    if ref and ref != "n00000000000" and ref not in valid_ids:
                        failures.append((f, attr, ref, w.attrib.get(XML_ID)))

            val = w.attrib.get("frame", "")
            if val:
                for part in val.split(" "):
                    raw = FRAME_PREFIX_RE.sub("", part)
                    for ref in raw.split(";"):
                        if ref and ref != "n00000000000" and ref not in valid_ids:
                            failures.append((f, "frame", ref, w.attrib.get(XML_ID)))

    return failures


# Cross-book referent validity: @referent/@subjref/@frame may point to xml:ids
# in a different book, so we must validate against the full corpus, not per-file.
def test_nestle1904_cross_corpus_referent_ids():
    valid_ids = _collect_valid_ids(__lowfat_files__)
    failures = _check_referents(__lowfat_files__, valid_ids)
    assert not failures, \
        f"Dead cross-corpus referents in Nestle1904 (first 10): {failures[:10]}"


def test_sblgnt_cross_corpus_referent_ids():
    valid_ids = _collect_valid_ids(__sblgnt_lowfat_files__)
    failures = _check_referents(__sblgnt_lowfat_files__, valid_ids)
    assert not failures, \
        f"Dead cross-corpus referents in SBLGNT (first 10): {failures[:10]}"
