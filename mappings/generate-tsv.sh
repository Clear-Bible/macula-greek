#!/usr/bin/env bash
# Regenerate a MACULA Greek TSV from the lowfat XML via BaseX.
#
# Usage: ./mappings/generate-tsv.sh SBLGNT | Nestle1904 | all
#
# Two non-obvious flags are required, which is why this wrapper exists:
#
#   -O xinclude=true    The *lowfat.xml inputs are XInclude indexes pointing at
#                       the 27 per-book files, not merged corpora. BaseX >= 10
#                       defaults XINCLUDE to false, so without this the query
#                       matches no <w> and writes a header-only file.
#
#   -Djdk.xml.maxElementDepth=0
#                       The Luke 3:23-38 genealogy is a recursive NP-of-NP chain
#                       nesting <wg class="np"> 156 levels deep. JDK >= 24 caps
#                       element depth at 100 and aborts the parse with
#                       "JAXP00010006: The element "w" has a depth of "101"".
#                       0 means no limit.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

generate() {
  local corpus="$1" input output rows
  case "$corpus" in
    SBLGNT)
      input=SBLGNT/lowfat/sblgntlowfat.xml
      output=SBLGNT/tsv/macula-greek-SBLGNT.tsv
      ;;
    Nestle1904)
      input=Nestle1904/lowfat/nestle1904lowfat.xml
      output=Nestle1904/tsv/macula-greek-Nestle1904.tsv
      ;;
    *)
      echo "Unknown corpus: $corpus (expected SBLGNT, Nestle1904, or all)" >&2
      return 2
      ;;
  esac

  mkdir -p "$(dirname "$output")"
  BASEX_JVM="-Djdk.xml.maxElementDepth=0${BASEX_JVM:+ $BASEX_JVM}" \
    basex -O xinclude=true -i "$input" -o "$output" mappings/greek-lowfat-to-tsv.xq

  # Guard against the silent header-only result this wrapper exists to prevent.
  # BaseX writes no trailing newline, so `wc -l` equals the data row count.
  rows="$(wc -l < "$output" | tr -d "[:space:]")"
  if (( rows < 100000 )); then
    echo "$output has only $rows rows; XML parsing likely failed silently." >&2
    return 1
  fi
  echo "$output: $rows rows"
}

case "${1:-}" in
  all)
    generate SBLGNT
    generate Nestle1904
    ;;
  "")
    echo "Usage: $0 SBLGNT | Nestle1904 | all" >&2
    exit 2
    ;;
  *)
    generate "$1"
    ;;
esac
