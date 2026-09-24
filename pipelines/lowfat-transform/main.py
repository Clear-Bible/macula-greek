import concurrent.futures
import multiprocessing
import os
import sys
from pathlib import Path

from saxonche import PySaxonProcessor

try:
    REPO_ROOT = Path(__file__).parent.parent.parent
except NameError:
    REPO_ROOT = Path(os.getcwd()).parent.parent

MAX_WORKERS = int(os.environ.get("MAX_WORKERS", multiprocessing.cpu_count() - 1))
SERIAL = os.environ.get("SERIAL", "").lower() in ("1", "true", "yes")

# SaxonC 13 is built with GraalVM Native Image 25 (JDK 25), which enforces the
# JDK default of jdk.xml.maxElementDepth=100; SaxonC 12 was built on a JDK that
# did not. The Luke 3:23-38 genealogy is a recursive NP-of-NP chain nesting
# ~160 levels deep, so without lifting the cap 03-luke.xml aborts with
# `JAXP00010006: The element "Node" has a depth of "101"`. 0 means no limit.
# See test_transform.py, which pins this.
MAX_ELEMENT_DEPTH_PROPERTY = (
    "http://saxon.sf.net/feature/parserProperty?uri="
    "http://www.oracle.com/xml/jaxp/properties/maxElementDepth"
)


def nodes_xml_paths(nodes_dir):
    return sorted(nodes_dir.glob("*.xml"))


def transform(source, dest):
    proc = PySaxonProcessor(license=False)
    proc.set_configuration_property(MAX_ELEMENT_DEPTH_PROPERTY, "0")
    xqueryp = proc.new_xquery_processor()
    xqueryp.run_query_to_file(
        input_file_name=str(source),
        query_file=str(REPO_ROOT / "mappings/lowfat-macula-greek.xquery"),
        output_file_name=str(dest),
    )


def reformat(source):
    # Saxon already writes the XML declaration, the two stylesheet processing
    # instructions and the indentation (see `output:indent` in the XQuery), so
    # the only fix-up left is the milestone spacing. Saxon's trailing newline is
    # dropped to keep the committed files byte-identical.
    # TODO: Review milestone spacing?
    text = source.read_text()
    text = text.replace("</milestone>\n", "</milestone> \n")
    source.write_text(text.rstrip("\n"))


def do_transform(input_path, output_dir):
    print(f"transforming {input_path.name}")
    dest = output_dir / input_path.name
    transform(input_path, dest)
    print(f"reformatting {dest.name}")
    reformat(dest)


def serial_transform(nodes_dir, output_dir):
    # Runs in-process, so exceptions keep their traceback and `pdb`/`ipdb` are
    # usable. Set SERIAL=1 to choose this path.
    for node_path in nodes_xml_paths(nodes_dir):
        do_transform(node_path, output_dir)


def parallel_transform(nodes_dir, output_dir):
    exceptions = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        deferred_tasks = {}
        for node_path in nodes_xml_paths(nodes_dir):
            deferred = executor.submit(do_transform, node_path, output_dir)
            deferred_tasks[deferred] = node_path

        for f in concurrent.futures.as_completed(deferred_tasks):
            try:
                f.result()
            except Exception as exc:
                exceptions.append(exc)

    if exceptions:
        raise exceptions[0]


def main():
    edition = sys.argv[1]
    nodes_dir = REPO_ROOT / f"{edition}/nodes"
    assert nodes_dir.exists()

    lowfat_dir = REPO_ROOT / f"{edition}/lowfat"
    if SERIAL:
        serial_transform(nodes_dir, lowfat_dir)
    else:
        parallel_transform(nodes_dir, lowfat_dir)


if __name__ == "__main__":
    main()
