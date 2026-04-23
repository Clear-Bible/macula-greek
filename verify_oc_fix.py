#!/usr/bin/env python3
"""
verify_oc_fix.py — Independent verification of the O2→OC fix (issue #101).

Approach is DELIBERATELY DIFFERENT from fix_o2_to_oc.py:
  - Does not use nodeId matching at all.
  - For each Cat="O2" + Label="OC" node in trees-na27 (ignoring Label="IO"
    and Label="COMP"), it:
      1. Identifies the head word via UnicodeLemma and verse (from nodeId prefix).
      2. Searches the corresponding Nestle1904 and SBLGNT book file for a Cat="OC"
         node in the same verse whose head word matches.
  - Reports found / not-found for each, plus a global summary.
  - Also checks that NO Label attributes remain anywhere in either edition.

Book-number prefix mapping uses the two-digit book code at the start of each nodeId
(41 = Mark, 50 = Philippians, etc.) — the same books as SBLGNT/Nestle1904 filenames.
"""

from pathlib import Path
from lxml import etree

TREES_NA27 = Path("/Users/jonathan/github/Clear/trees/trees-na27/trees")
MACULA_GREEK = Path("/Users/jonathan/github/Clear/macula-greek")
NESTLE1904_NODES = MACULA_GREEK / "Nestle1904/nodes"
SBLGNT_NODES = MACULA_GREEK / "SBLGNT/nodes"

# nodeId two-digit prefix → (book-number-in-filename, filename-stem)
# The NT book list in macula-greek uses 01-matthew.xml … 27-revelation.xml
BOOK_MAP = {
    "40": ("01", "matthew"),
    "41": ("02", "mark"),
    "42": ("03", "luke"),
    "43": ("04", "john"),
    "44": ("05", "acts"),
    "45": ("06", "romans"),
    "46": ("07", "1corinthians"),
    "47": ("08", "2corinthians"),
    "48": ("09", "galatians"),
    "49": ("10", "ephesians"),
    "50": ("11", "philippians"),
    "51": ("12", "colossians"),
    "52": ("13", "1thessalonians"),
    "53": ("14", "2thessalonians"),
    "54": ("15", "1timothy"),
    "55": ("16", "2timothy"),
    "56": ("17", "titus"),
    "57": ("18", "philemon"),
    "58": ("19", "hebrews"),
    "59": ("20", "james"),
    "60": ("21", "1peter"),
    "61": ("22", "2peter"),
    "62": ("23", "1john"),
    "63": ("24", "2john"),
    "64": ("25", "3john"),
    "65": ("26", "jude"),
    "66": ("27", "revelation"),
}


def find_macula_file(edition_dir, node_id_prefix):
    num, name = BOOK_MAP[node_id_prefix[:2]]
    pattern = f"{num}-{name}.xml"
    path = edition_dir / pattern
    return path if path.exists() else None


def get_head_lemma(node):
    """Return the UnicodeLemma of the deepest/head leaf inside this node."""
    # Walk into children; prefer the node marked Head="1" or the last leaf.
    # Trees-na27 leaf nodes carry UnicodeLemma directly.
    leaf_lemma = node.get("UnicodeLemma")
    for child in node:
        child_lemma = get_head_lemma(child)
        if child_lemma:
            leaf_lemma = child_lemma
    return leaf_lemma


def verse_prefix(node_id):
    """Return the 8-char verse identifier from a nodeId."""
    return node_id[:8] if len(node_id) >= 8 else node_id


def build_oc_targets():
    """
    Returns list of dicts for every Cat="O2" + Label="OC" node in trees-na27.
    Ignores Label="IO" and Label="COMP".
    Each dict: {node_id, verse, head_lemma, rule, book_prefix}
    """
    targets = []
    for f in sorted(TREES_NA27.glob("*.xml")):
        for node in etree.parse(str(f)).iter("Node"):
            if node.get("Cat") != "O2":
                continue
            label = node.get("Label", "")
            if label in ("IO", "COMP", ""):
                continue          # only interested in OC
            if label != "OC":
                continue
            nid = node.get("nodeId", "")
            if not nid or nid[:2] not in BOOK_MAP:
                continue
            targets.append({
                "node_id":    nid,
                "verse":      verse_prefix(nid),
                "head_lemma": get_head_lemma(node),
                "rule":       node.get("Rule", ""),
                "book_prefix": nid[:2],
            })
    return targets


def build_oc_index(edition_dir):
    """
    Parse all files in edition_dir; return dict:
      verse_prefix → list of (UnicodeLemma, Rule) pairs for Cat="OC" nodes
    Also build a 'bad' set of nodeIds that still carry Label.
    """
    oc_index = {}      # verse → [(head_lemma, rule), ...]
    label_count = 0
    for filepath in sorted(edition_dir.glob("*.xml")):
        tree = etree.parse(str(filepath))
        for node in tree.iter("Node"):
            if node.get("Label") is not None:
                label_count += 1
            if node.get("Cat") == "OC":
                nid = node.get("nodeId", "")
                v = verse_prefix(nid) if nid else ""
                head_lemma = get_head_lemma(node)
                rule = node.get("Rule", "")
                oc_index.setdefault(v, []).append((head_lemma, rule))
    return oc_index, label_count


def check_target(target, oc_index):
    """
    Return True if the target is found in the given OC index.
    Matching: same verse AND same head_lemma (case-sensitive).
    Falls back to same-verse + same-Rule if lemma alone is ambiguous.
    """
    verse = target["verse"]
    expected_lemma = target["head_lemma"]
    expected_rule = target["rule"]

    if verse not in oc_index:
        return False

    entries = oc_index[verse]

    # Primary: same verse + same head lemma
    lemma_matches = [e for e in entries if e[0] == expected_lemma]
    if lemma_matches:
        return True

    # Fallback: same verse + same rule pattern (O2→OC substitution already applied)
    expected_rule_oc = expected_rule.replace("O2", "OC")
    rule_matches = [e for e in entries if e[1] == expected_rule_oc]
    return bool(rule_matches)


def main():
    print("Building OC target list from trees-na27 …")
    targets = build_oc_targets()
    print(f"  {len(targets)} Cat='O2'+Label='OC' nodes (ignoring IO/COMP)\n")

    print("Indexing Nestle1904 OC nodes …")
    n1904_index, n1904_labels = build_oc_index(NESTLE1904_NODES)
    print("Indexing SBLGNT OC nodes …")
    sblgnt_index, sblgnt_labels = build_oc_index(SBLGNT_NODES)

    # --- Label check ---
    print()
    if n1904_labels == 0:
        print("PASS  Nestle1904: no Label attributes found")
    else:
        print(f"FAIL  Nestle1904: {n1904_labels} Label attributes remain!")

    if sblgnt_labels == 0:
        print("PASS  SBLGNT: no Label attributes found")
    else:
        print(f"FAIL  SBLGNT: {sblgnt_labels} Label attributes remain!")

    # --- OC coverage check ---
    n1904_found = 0
    sblgnt_found = 0
    n1904_missing = []
    sblgnt_missing = []

    for t in targets:
        if check_target(t, n1904_index):
            n1904_found += 1
        else:
            n1904_missing.append(t)
        if check_target(t, sblgnt_index):
            sblgnt_found += 1
        else:
            sblgnt_missing.append(t)

    print()
    print(f"Nestle1904: {n1904_found}/{len(targets)} OC targets confirmed as Cat='OC'")
    print(f"SBLGNT:     {sblgnt_found}/{len(targets)} OC targets confirmed as Cat='OC'")

    if n1904_missing:
        print(f"\nNestle1904 NOT FOUND ({len(n1904_missing)}):")
        for t in n1904_missing:
            print(f"  verse={t['verse']}  lemma={t['head_lemma']}  rule={t['rule']}  id={t['node_id']}")

    if sblgnt_missing:
        print(f"\nSBLGNT NOT FOUND ({len(sblgnt_missing)}):")
        for t in sblgnt_missing:
            print(f"  verse={t['verse']}  lemma={t['head_lemma']}  rule={t['rule']}  id={t['node_id']}")

    if not n1904_missing and not sblgnt_missing and n1904_labels == 0 and sblgnt_labels == 0:
        print("\nAll checks passed.")


if __name__ == "__main__":
    main()
