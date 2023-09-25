import concurrent.futures
import json
import multiprocessing
import os
import re
from itertools import groupby
from operator import itemgetter
from pathlib import Path

from lxml import etree


try:
    REPO_ROOT = Path(__file__).parent.parent.parent
except NameError:
    REPO_ROOT = Path(os.getcwd()).parent.parent

PIPELINE_ROOT = REPO_ROOT / "pipelines" / "tei-transform"
FIXTURES_ROOT = PIPELINE_ROOT / "fixtures"
MAX_WORKERS = int(os.environ.get("MAX_WORKERS", multiprocessing.cpu_count() - 1))

# TODO: Refactor into generic library code
BOOK_LOOKUP_PATH = FIXTURES_ROOT / "bible-books-lookup.json"
BOOK_DATA = json.load(BOOK_LOOKUP_PATH.open())

XML_PATH = REPO_ROOT / "sources/LogosBible/SBLGNT/data/sblgnt/xml"
TEI_PATH = REPO_ROOT / "SBLGNT/tei"


# TODO: Refactor into generic library code
USFM_REF_PATTERN = re.compile(
    r"(?P<book>[A-Z1-4]{3})(\s(?P<chapter>\d+))?(:(?P<verse>\d+))?(!(?P<position>\d+))?"  # noqa
)


XML_NS = "{http://www.w3.org/XML/1998/namespace}"


XSL_STYLESHEET_PATH = FIXTURES_ROOT / "sblgnt-tei.xsl"


LOGOS_PATH_TO_USFM_LOOKUP = {
    "1Cor.xml": "1CO",
    "1John.xml": "1JN",
    "1Pet.xml": "1PE",
    "1Thess.xml": "1TH",
    "1Tim.xml": "1TI",
    "2Cor.xml": "2CO",
    "2John.xml": "2JN",
    "2Pet.xml": "2PE",
    "2Thess.xml": "2TH",
    "2Tim.xml": "2TI",
    "3John.xml": "3JN",
    "Acts.xml": "ACT",
    "Col.xml": "COL",
    "Eph.xml": "EPH",
    "Gal.xml": "GAL",
    "Heb.xml": "HEB",
    "Jas.xml": "JAS",
    "John.xml": "JHN",
    "Jude.xml": "JUD",
    "Luke.xml": "LUK",
    "Mark.xml": "MRK",
    "Matt.xml": "MAT",
    "Phil.xml": "PHP",
    "Phlm.xml": "PHM",
    "Rev.xml": "REV",
    "Rom.xml": "ROM",
    "Titus.xml": "TIT",
}

USFM_TO_MACULA_PATH_LOOKUP = {
    "MAT": "01-matthew.xml",
    "MRK": "02-mark.xml",
    "LUK": "03-luke.xml",
    "JHN": "04-john.xml",
    "ACT": "05-acts.xml",
    "ROM": "06-romans.xml",
    "1CO": "07-1corinthians.xml",
    "2CO": "08-2corinthians.xml",
    "GAL": "09-galatians.xml",
    "EPH": "10-ephesians.xml",
    "PHP": "11-philippians.xml",
    "COL": "12-colossians.xml",
    "1TH": "13-1thessalonians.xml",
    "2TH": "14-2thessalonians.xml",
    "1TI": "15-1timothy.xml",
    "2TI": "16-2timothy.xml",
    "TIT": "17-titus.xml",
    "PHM": "18-philemon.xml",
    "HEB": "19-hebrews.xml",
    "JAS": "20-james.xml",
    "1PE": "21-1peter.xml",
    "2PE": "22-2peter.xml",
    "1JN": "23-1john.xml",
    "2JN": "24-2john.xml",
    "3JN": "25-3john.xml",
    "JUD": "26-jude.xml",
    "REV": "27-revelation.xml",
}


# TODO: Refactor into generic library code
def bcvw_ref_generator(book_data, ref):
    testament_prefix = book_data["testament"].lower()[0:1]
    match = USFM_REF_PATTERN.match(ref).groupdict()
    book = book_data["ord"].ljust(2, "0")
    chapter = f'{match["chapter"]}'.zfill(3)
    verse = f'{match["verse"]}'.zfill(3)
    word = f'{match["position"]}'.zfill(3)
    return f"{testament_prefix}{book}{chapter}{verse}{word}"


class XSLTransformer:
    def __init__(self, book_usfm_ref, xml):
        self.book_usfm_ref = book_usfm_ref
        self.xml = xml
        self.book = list(filter(lambda x: x["abbr"] == self.book_usfm_ref, BOOK_DATA))[0]

        self.chapter = None
        self.last_verse = None
        self.words_by_verse = {}
        self.words = []

    def render(self):
        with XSL_STYLESHEET_PATH.open("rb") as f:
            func_ns = "urn:python-funcs"
            transform = etree.XSLT(
                etree.XML(f.read()),
                extensions={
                    (func_ns, "usfm_ref"): self.usfm_ref,
                    (func_ns, "regroup_elements_to_chapters"): self.regroup_elements_to_chapters,
                    (func_ns, "word_transform"): self.word_transform,
                    (func_ns, "chapter_transform"): self.chapter_transform,
                    (func_ns, "get_book_usfm_ref"): self.get_book_usfm_ref,
                    (func_ns, "get_chapter_usfm_ref"): self.get_chapter_usfm_ref,
                },
            )
            try:
                return str(transform(self.xml))
            except Exception:
                import ipdb

                ipdb.set_trace()
                for error in transform.error_log:
                    print(error.message, error.line)
                raise

    def usfm_ref(self, ctx, value):
        node = value[0]
        id_val = node.attrib.pop("id")
        try:
            _, rest = id_val.rsplit(maxsplit=1)
        except Exception:
            import pdb

            pdb.set_trace()

        ref = f'{self.book["abbr"]} {rest}'
        if self.last_verse is not None and self.last_verse.attrib["ref"] == ref:
            return None

        node.set("ref", ref)
        self.words_by_verse[ref] = self.words
        self.words = []
        self.last_verse = node
        return ref

    def get_book_usfm_ref(self, ctx, value):
        return self.book_usfm_ref

    def get_chapter_usfm_ref(self, ctx, chapter, book_part):
        return f"{chapter} {book_part.rsplit()[-1]}"

    def chapter_transform(self, ctx, value):
        elem = value[0]
        self.chapter = elem
        return elem

    @staticmethod
    def chapter_title_text(elem, chapter_ref):
        try:
            prefix = elem.attrib["id"].split(" ")[1].split(":")[0]
        except:
            prefix = ""
        if prefix == chapter_ref:
            text = chapter_ref
        else:
            text = f"{prefix} {chapter_ref}".strip()
        return text

    def regroup_elements_to_chapters(self, ctx, value):
        chapters = []
        for chapter_ref, paragraphs_iter in get_chapters(value[0]):
            # FIXME: This is transient so we can set title text
            # for diff purposes
            paragraphs = list(paragraphs_iter)

            chapter = etree.Element("chapter")
            chapter.set("ref", f"{self.book_usfm_ref} {chapter_ref}")
            title = etree.Element("title")
            title.text = self.chapter_title_text(paragraphs[0][1][0], chapter_ref)
            chapter.append(title)

            for _, elements in paragraphs:
                p = etree.Element("p")
                for element in elements:
                    p.append(element)
                chapter.append(p)
            chapters.append(chapter)
        return chapters

    def word_transform(self, ctx, value):
        elem = value[0]
        position = len(self.words) + 1
        verse_ref = self.last_verse.attrib["ref"]
        word_ref = f"{verse_ref}!{position}"
        elem.attrib["ref"] = word_ref
        elem.attrib[f"{XML_NS}id"] = bcvw_ref_generator(self.book, word_ref)
        self.words.append(elem.text)
        return elem


def get_source_paths():
    for path in XML_PATH.glob("*.xml"):
        if path.name in LOGOS_PATH_TO_USFM_LOOKUP:
            yield path


def get_chapters(parsed):
    last_chapter = None
    regrouped_paragraphs = []
    words_before = []
    for p in parsed.xpath("//p"):
        for child in p.getchildren():
            if child.tag == "verse-number":
                verse = child
            else:
                if not last_chapter:
                    words_before.append(child)
                    continue

            current_verse = verse.attrib["id"]
            current_chapter = current_verse.rsplit(" ", maxsplit=1)[1].split(":")[0]
            if not last_chapter:
                paragraph = [current_chapter, []]
            if last_chapter and current_chapter != last_chapter:
                regrouped_paragraphs.append(paragraph)
                paragraph = [current_chapter, []]
            if words_before:
                paragraph[1].extend(words_before)
            paragraph[1].append(verse)
            last_chapter = current_chapter
            following_siblings = verse.xpath("following-sibling::*")
            elements_between = []
            for sibling in following_siblings:
                if sibling.tag == "verse-number":
                    break
                elements_between.append(sibling)
            paragraph[1].extend(elements_between)
        regrouped_paragraphs.append(paragraph)
        last_chapter = None
        words_before = []
    return groupby(regrouped_paragraphs, key=itemgetter(0))


def do_transform(source):
    print(f"transforming {source.name}")
    usfm_ref = LOGOS_PATH_TO_USFM_LOOKUP[source.name]
    dest_name = USFM_TO_MACULA_PATH_LOOKUP[usfm_ref]
    dest = TEI_PATH / dest_name
    transformer = XSLTransformer(usfm_ref, etree.parse(source.open("rb")))
    with dest.open("w") as f:
        f.write(transformer.render())


def serial_transform():
    for source_path in get_source_paths():
        do_transform(source_path)


def parallel_transform():
    exceptions = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        deferred_tasks = {}
        for source_path in get_source_paths():
            deferred = executor.submit(do_transform, source_path)
            deferred_tasks[deferred] = source_path

        for f in concurrent.futures.as_completed(deferred_tasks):
            try:
                f.result()
            except Exception as exc:
                exceptions.append(exc)

    if exceptions:
        raise exceptions[0]


def main():
    TEI_PATH.mkdir(parents=True, exist_ok=True)
    parallel_transform()


if __name__ == "__main__":
    main()
