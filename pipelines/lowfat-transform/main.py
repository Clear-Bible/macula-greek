import os
import shlex
import subprocess
from pathlib import Path
import concurrent.futures
import multiprocessing

from saxonche import PySaxonProcessor

# NOTE: Override BaseX binary path
BASEX_BINARY = os.environ.get("BASEX_BINARY", "basex")
try:
    REPO_ROOT = Path(__file__).parent.parent.parent
except:
    REPO_ROOT = Path(os.getcwd()).parent.parent

NODES_PATH = REPO_ROOT / "Nestle1904/nodes"
LOWFAT_PATH = REPO_ROOT / "Nestle1904/lowfat"
MAX_WORKERS = int(os.environ.get("MAX_WORKERS", multiprocessing.cpu_count() - 1))


def nodes_xml_paths():
    return sorted(NODES_PATH.glob("*.xml"))


def transform(source, dest):
    # TODO: See if we might replace BaseX calls with Saxon calls
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


def legacy():
    """
    time ./transform-to-lowfat.sh
    ./transform-to-lowfat.sh  214.55s user 17.24s system 188% cpu 2:02.72 total
    python main.py  231.36s user 19.60s system 188% cpu 2:12.84 total
    """
    cmd = shlex.split("bash transform-to-lowfat.sh")
    subprocess.run(cmd, cwd=REPO_ROOT)


def serial():
    for node_path in nodes_xml_paths():
        do_transform(node_path)


def parallel_processes():
    """
    7 workers on 8 core machine
    python main.py  423.39s user 43.17s system 669% cpu 1:09.66 total
    4 workers on 8 core machine
    python main.py  414.45s user 41.34s system 599% cpu 1:16.04 total
    """
    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for node_path in nodes_xml_paths():
            executor.submit(do_transform, node_path)


def parallel_threads():
    """
    python main.py  376.83s user 39.56s system 706% cpu 58.965 total
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for node_path in nodes_xml_paths():
            executor.submit(do_transform, node_path)


def main():
    parallel_processes()
    # legacy()
    # parallel_threads()
    # serial()


if __name__ == "__main__":
    main()
