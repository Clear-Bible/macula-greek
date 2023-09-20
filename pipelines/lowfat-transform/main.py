import concurrent.futures
import multiprocessing
import os
import shlex
import subprocess
from pathlib import Path

from saxonche import PySaxonProcessor

# NOTE: Override BaseX binary path
BASEX_BINARY = os.environ.get("BASEX_BINARY", "basex")
try:
    REPO_ROOT = Path(__file__).parent.parent.parent
except:
    REPO_ROOT = Path(os.getcwd()).parent.parent

# TODO: remove hard-coding to Nestle1904
NODES_PATH = REPO_ROOT / "Nestle1904/nodes"
LOWFAT_PATH = REPO_ROOT / "Nestle1904/lowfat"
MAX_WORKERS = int(os.environ.get("MAX_WORKERS", multiprocessing.cpu_count() - 1))
USE_SAXON = bool(int(os.environ.get("USE_SAXON", "0")))


def nodes_xml_paths():
    return sorted(NODES_PATH.glob("*.xml"))


def transform(source, dest):
    if USE_SAXON:
        proc = PySaxonProcessor(license=False)
        proc.new_xquery_processor()
        xqueryp = proc.new_xquery_processor()
        xqueryp.run_query_to_file(
            input_file_name=str(source),
            query_file=str(REPO_ROOT / "mappings/lowfat-macula-greek.xquery"),
            output_file_name=str(dest),
        )

    else:
        # TODO: Support BaseX within GitHub actions using Docker-in-Docker
        parts = [
            BASEX_BINARY,
            "-W",
            "-i",
            source,
            REPO_ROOT / "mappings/lowfat-macula-greek.xquery",
        ]
        cmd = shlex.split(" ".join([str(s) for s in parts]))
        with dest.open("w") as f:
            subprocess.run(cmd, stdout=f)


def reformat(source):
    proc = PySaxonProcessor(license=False)
    parsed = proc.parse_xml(xml_text=source.read_text())
    temp = proc.get_string_value(parsed)
    # re-insert newlines
    temp = temp.replace(
        '<?xml-stylesheet href="treedown.css"?><?xml-stylesheet href="boxwood.css"?>',
        '<?xml-stylesheet href="treedown.css"?>\n<?xml-stylesheet href="boxwood.css"?>\n',
    )
    source.write_text(temp)
    # re-insert declaration
    temp = f'<?xml version="1.0" encoding="UTF-8"?>{temp}'
    source.write_text(temp)
    temp = proc.get_string_value(parsed)
    temp = temp.replace(
        '<?xml-stylesheet href="treedown.css"?><?xml-stylesheet href="boxwood.css"?>',
        '<?xml-stylesheet href="treedown.css"?>\n<?xml-stylesheet href="boxwood.css"?>\n',
    )
    temp = f'<?xml version="1.0" encoding="UTF-8"?>\n{temp}'
    # TODO: Review milestone spacing?
    temp = temp.replace("</milestone>\n", "</milestone> \n")
    source.write_text(temp)


def do_transform(source):
    print(f"transforming {source.name}")
    dest = LOWFAT_PATH / source.name
    transform(source, dest)
    print(f"reformatting {dest.name}")
    reformat(dest)


def serial_transform():
    for node_path in nodes_xml_paths():
        do_transform(node_path)


def parallel_transform():
    exceptions = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        deferred_tasks = {}
        for node_path in nodes_xml_paths():
            deferred = executor.submit(do_transform, node_path)
            deferred_tasks[deferred] = node_path

        for f in concurrent.futures.as_completed(deferred_tasks):
            try:
                f.result()
            except Exception as exc:
                exceptions.append(exc)

    if exceptions:
        raise exceptions[0]


def main():
    parallel_transform()


if __name__ == "__main__":
    main()
