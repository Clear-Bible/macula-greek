import os
import sys
from pathlib import Path

from saxonche import PySaxonProcessor

try:
    REPO_ROOT = Path(__file__).parent.parent.parent
except NameError:
    REPO_ROOT = Path(os.getcwd()).parent.parent

QUERY = REPO_ROOT / "mappings/greek-lowfat-to-tsv.xq"

# (lowfat input, TSV output), both relative to REPO_ROOT. The index file names
# are irregular enough not to be worth deriving, and spelling them out makes
# this double as the set of valid command-line arguments. SBLGNT comes first to
# match the order the `all` run used to print in.
EDITIONS = {
    "SBLGNT": (
        Path("SBLGNT/lowfat/sblgntlowfat.xml"),
        Path("SBLGNT/tsv/macula-greek-SBLGNT.tsv"),
    ),
    "Nestle1904": (
        Path("Nestle1904/lowfat/nestle1904lowfat.xml"),
        Path("Nestle1904/tsv/macula-greek-Nestle1904.tsv"),
    ),
}

# Both corpora hold about 137,700 data rows, one per <w> in the lowfat. A
# result near zero is a parse that failed quietly, not a data change.
MINIMUM_ROWS = 100000

# Saxon's short name for the XInclude configuration feature, which is off by
# default. The inputs above are XInclude indexes over the 27 per-book files,
# not merged corpora, so without this `//w` matches nothing and the query
# writes a 173-byte file holding only its header row. MINIMUM_ROWS is the
# backstop for exactly that.
XINCLUDE_PROPERTY = "xi"

# SaxonC 13 is built with GraalVM Native Image 25 (JDK 25), which enforces the
# JDK default of jdk.xml.maxElementDepth=100. The Luke 3:23-38 genealogy is a
# recursive NP-of-NP chain nesting <wg class="np"> about 160 levels deep, so
# the parse aborts without this. 0 means no limit.
#
# The resulting error names the wrong thing: the native image ships no
# XInclude message bundle, so the failure surfaces as `Could not load any
# resource bundle by ...impl.msg.XIncludeMessages` and the real
# `JAXP00010006` depth error only appears on stderr.
MAX_ELEMENT_DEPTH_PROPERTY = (
    "http://saxon.sf.net/feature/parserProperty?uri="
    "http://www.oracle.com/xml/jaxp/properties/maxElementDepth"
)


def transform(source, dest):
    proc = PySaxonProcessor(license=False)
    proc.set_configuration_property(XINCLUDE_PROPERTY, "on")
    proc.set_configuration_property(MAX_ELEMENT_DEPTH_PROPERTY, "0")
    xqueryp = proc.new_xquery_processor()
    # Serialization is set here rather than in the query, so the query stays
    # portable to any XQuery processor. It returns a sequence of tab-joined
    # strings; Saxon's default would serialize that as XML, with a declaration
    # and space-separated items. `text` plus a newline item separator writes
    # the TSV directly and leaves the last row unterminated, which is how the
    # committed files are stored.
    xqueryp.set_property("!method", "text")
    xqueryp.set_property("!item-separator", "\n")
    xqueryp.set_property("!omit-xml-declaration", "yes")
    xqueryp.run_query_to_file(
        input_file_name=str(source),
        query_file=str(QUERY),
        output_file_name=str(dest),
    )


def check_row_count(dest):
    # There is a newline after the header and after every data row except the
    # last, so the newline count is exactly the number of data rows. This is
    # the same quantity `wc -l` reported for the BaseX output it replaced.
    rows = dest.read_text(encoding="utf-8").count("\n")
    if rows < MINIMUM_ROWS:
        raise SystemExit(f"{dest} has only {rows} rows; XML parsing likely failed silently.")
    return rows


def do_transform(edition):
    source, dest = (REPO_ROOT / part for part in EDITIONS[edition])
    assert source.exists()

    print(f"transforming {source.name}")
    transform(source, dest)
    print(f"{dest.name}: {check_row_count(dest)} rows")


def main():
    argument = sys.argv[1] if len(sys.argv) > 1 else ""
    if argument == "all":
        editions = list(EDITIONS)
    elif argument in EDITIONS:
        editions = [argument]
    else:
        raise SystemExit(f"Usage: {sys.argv[0]} {' | '.join(EDITIONS)} | all")

    for edition in editions:
        do_transform(edition)


if __name__ == "__main__":
    main()
