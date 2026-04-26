#!/usr/bin/env python3
"""
fix_o2_to_oc.py — Resolve issue #101: distinguish OC (object complement)
from genuine O2 (second object).

Design decisions:
  - Cat="O2" → Cat="OC" on O2 phrase nodes identified as object complements
  - Rule pattern: replace "O2" with "OC" in the Rule value of those same nodes
    (e.g. CL2O2x → CL2OCx, Np2O2 → Np2OC, adjp2O2 → adjp2OC)
  - Label attribute removed entirely from all nodes (Label is a GBI-internal
    annotation and should not appear in macula-greek)

Source of truth for OC identity:
  - SBLGNT:    Cat="O2" phrase nodes whose subtree contains any Label="OC" leaf
  - Nestle1904: Cat="O2" phrase nodes matching trees-na27 Cat="O2"+Label="OC"
                by nodeId (primary) or verse+suffix fallback

Whitespace preservation: lxml identifies which nodes to fix; raw string
replacement writes the changes so that original XML formatting is untouched.
"""

import re
import sys
from pathlib import Path
from lxml import etree

TREES_NA27 = Path("/Users/jonathan/github/Clear/trees/trees-na27/trees")
MACULA_GREEK = Path("/Users/jonathan/github/Clear/macula-greek")
NESTLE1904_NODES = MACULA_GREEK / "Nestle1904/nodes"
SBLGNT_NODES = MACULA_GREEK / "SBLGNT/nodes"

DRY_RUN = "--dry-run" in sys.argv


# ---------------------------------------------------------------------------
# Build OC node set from trees-na27
# ---------------------------------------------------------------------------

def build_trees_sets():
    """Return (oc_ids, genuine_o2_ids) from trees-na27.
    oc_ids:        Cat="O2" + Label="OC"
    genuine_o2_ids: Cat="O2" + Label!="OC" (including empty Label)
    """
    oc_ids = set()
    genuine_o2_ids = set()
    for f in sorted(TREES_NA27.glob("*.xml")):
        for node in etree.parse(f).iter("Node"):
            if node.get("Cat") != "O2":
                continue
            nid = node.get("nodeId", "")
            if not nid:
                continue
            if node.get("Label") == "OC":
                oc_ids.add(nid)
            else:
                genuine_o2_ids.add(nid)
    return oc_ids, genuine_o2_ids


# ---------------------------------------------------------------------------
# String-level helpers (preserve whitespace)
# ---------------------------------------------------------------------------

def find_elem_tag_bounds(text, node_id):
    """Return (elem_start, tag_end) for the opening tag of the element
    whose nodeId attribute equals node_id, or (None, None) if not found."""
    id_str = f'nodeId="{node_id}"'
    pos = text.find(id_str)
    if pos == -1:
        return None, None
    elem_start = text.rfind("<Node", 0, pos)
    if elem_start == -1:
        return None, None
    tag_end = text.find(">", pos)
    if tag_end == -1:
        return None, None
    return elem_start, tag_end


def change_cat_o2_to_oc_and_update_rule(text, node_id):
    """Change Cat="O2"→Cat="OC" and replace O2→OC inside the Rule value
    on the element identified by node_id.  Returns (new_text, changed_bool)."""
    elem_start, tag_end = find_elem_tag_bounds(text, node_id)
    if elem_start is None:
        return text, False

    opening_tag = text[elem_start : tag_end + 1]
    if 'Cat="O2"' not in opening_tag:
        return text, False

    new_tag = opening_tag.replace('Cat="O2"', 'Cat="OC"', 1)
    # Update the Rule value: replace every "O2" token inside the quoted value
    new_tag = re.sub(r'(Rule="[^"]*?)O2', r'\1OC', new_tag)

    return text[:elem_start] + new_tag + text[tag_end + 1 :], True


def remove_label_attr(text, node_id):
    """Remove the Label="..." attribute (any value) from the element
    identified by node_id.  Returns (new_text, removed_bool)."""
    elem_start, tag_end = find_elem_tag_bounds(text, node_id)
    if elem_start is None:
        return text, False

    opening_tag = text[elem_start : tag_end + 1]
    # Match Label="anything" with optional leading/trailing space
    new_tag, n = re.subn(r'\s+Label="[^"]*"', "", opening_tag, count=1)
    if n == 0:
        new_tag, n = re.subn(r'Label="[^"]*"\s*', "", opening_tag, count=1)
    if n == 0:
        return text, False

    return text[:elem_start] + new_tag + text[tag_end + 1 :], True


# ---------------------------------------------------------------------------
# Per-file fix routines
# ---------------------------------------------------------------------------

def fix_sblgnt_file(filepath):
    """
    SBLGNT strategy:
      1. O2 phrase nodes whose subtree has Label="OC" → Cat→OC, Rule→OC
      2. Remove ALL Label attributes from every node in the file
    Returns (oc_changed, labels_removed).
    """
    tree = etree.parse(str(filepath))
    oc_phrase_ids = []
    all_label_ids = []

    for node in tree.iter("Node"):
        nid = node.get("nodeId", "")
        if node.get("Cat") == "O2":
            has_oc_descendant = any(
                d.get("Label") == "OC"
                for d in node.iter("Node")
                if d is not node
            )
            if has_oc_descendant and nid:
                oc_phrase_ids.append(nid)
        if node.get("Label") is not None and nid:
            all_label_ids.append(nid)

    if DRY_RUN:
        print(
            f"  [DRY RUN] {filepath.name}: "
            f"{len(oc_phrase_ids)} O2→OC, {len(all_label_ids)} Label attrs to remove"
        )
        return len(oc_phrase_ids), len(all_label_ids)

    text = filepath.read_text(encoding="utf-8")
    oc_changed = 0
    for nid in oc_phrase_ids:
        text, ok = change_cat_o2_to_oc_and_update_rule(text, nid)
        if ok:
            oc_changed += 1
        else:
            print(f"  WARNING: Cat change failed for nodeId={nid} in {filepath.name}")

    labels_removed = 0
    for nid in all_label_ids:
        text, ok = remove_label_attr(text, nid)
        if ok:
            labels_removed += 1

    filepath.write_text(text, encoding="utf-8")
    return oc_changed, labels_removed


def fix_nestle1904_file(filepath, oc_set, genuine_o2_set):
    """
    Nestle1904 strategy:
      Match Cat="O2" nodes against trees-na27 OC set.
      Primary:  exact nodeId match against oc_set.
      Skip:     nodeId confirmed as genuine O2 in trees-na27 (genuine_o2_set).
      Fallback: same verse (first 8 chars) + same suffix (last 4 chars),
                only when unambiguous (exactly one OC candidate).
    Returns (changed, unmatched_list).
    """
    tree = etree.parse(str(filepath))
    to_fix = []
    unmatched = []

    for node in tree.iter("Node"):
        if node.get("Cat") != "O2":
            continue
        node_id = node.get("nodeId", "")

        if node_id in oc_set:
            to_fix.append(node_id)
            continue

        # If trees-na27 explicitly has this nodeId as genuine O2, keep it.
        if node_id in genuine_o2_set:
            unmatched.append(node_id)
            continue

        # Truly unmatched nodeId — try verse+suffix fallback (unambiguous only)
        if len(node_id) >= 8:
            verse = node_id[:8]
            suffix = node_id[-4:]
            candidates = [oc for oc in oc_set if oc[:8] == verse and oc[-4:] == suffix]
            if len(candidates) == 1:
                print(
                    f"  FALLBACK {filepath.name}: "
                    f"Nestle1904 {node_id} ↔ trees-na27 {candidates[0]}"
                )
                to_fix.append(node_id)
                continue
            elif len(candidates) > 1:
                print(f"  AMBIGUOUS fallback for {node_id} in {filepath.name}")

        unmatched.append(node_id)

    if DRY_RUN:
        print(
            f"  [DRY RUN] {filepath.name}: "
            f"{len(to_fix)} O2→OC, {len(unmatched)} unmatched"
        )
        return len(to_fix), unmatched

    text = filepath.read_text(encoding="utf-8")
    changed = 0
    for nid in to_fix:
        text, ok = change_cat_o2_to_oc_and_update_rule(text, nid)
        if ok:
            changed += 1
        else:
            print(f"  WARNING: Cat change failed for nodeId={nid} in {filepath.name}")

    if changed:
        filepath.write_text(text, encoding="utf-8")
    return changed, unmatched


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Building OC / genuine-O2 sets from trees-na27 …")
    oc_set, genuine_o2_set = build_trees_sets()
    print(f"  {len(oc_set)} OC nodes, {len(genuine_o2_set)} genuine-O2 nodes in trees-na27\n")

    print("=== SBLGNT ===")
    sblgnt_oc = 0
    sblgnt_labels = 0
    for filepath in sorted(SBLGNT_NODES.glob("*.xml")):
        changed, labels = fix_sblgnt_file(filepath)
        if changed or labels:
            print(f"  {filepath.name}: {changed} O2→OC, {labels} Label attrs removed")
        sblgnt_oc += changed
        sblgnt_labels += labels
    print(f"\nSBLGNT totals: {sblgnt_oc} O2→OC changes, {sblgnt_labels} Label attrs removed\n")

    print("=== Nestle1904 ===")
    nestle_oc = 0
    all_unmatched = []
    for filepath in sorted(NESTLE1904_NODES.glob("*.xml")):
        changed, unmatched = fix_nestle1904_file(filepath, oc_set, genuine_o2_set)
        if changed:
            print(f"  {filepath.name}: {changed} O2→OC")
        nestle_oc += changed
        all_unmatched.extend((filepath.name, nid) for nid in unmatched)
    print(f"\nNestle1904 totals: {nestle_oc} O2→OC changes")

    if all_unmatched:
        print(f"\nUnmatched Nestle1904 O2 nodes left as O2 ({len(all_unmatched)}):")
        for fname, nid in all_unmatched:
            print(f"  {fname}: {nid}")
    else:
        print("All Nestle1904 O2 nodes matched or left as genuine O2.")


if __name__ == "__main__":
    main()
