# MARBLE / Semantic Dictionary of Biblical Greek (SDBG)

## What it is

The [Semantic Dictionary of Biblical Greek (SDBG)](https://semanticdictionary.org/) is produced by the United Bible Societies [MARBLE](https://semanticdictionary.org/) project. It extends the semantic domain system of Louw & Nida's *Greek-English Lexicon of the New Testament Based on Semantic Domains* (New York: United Bible Societies, 1996) and provides word-sense assignments for each word occurrence in the Greek New Testament.

## How it is used here

SDBG data appears in two attributes on `<w>` elements in the lowfat and TSV output:

| Attribute | Content | Example |
|-----------|---------|---------|
| `@domain` | Six-digit SDBG domain code | `089007` |
| `@ln` | Louw & Nida entry number | `89.32` |

Example:
```xml
<w ref="LUK 1:1!1"
   lemma="ἐπειδήπερ"
   domain="089007"
   ln="89.32"
   gloss="Inasmuch as" .../>
```

### Domain codes

The `@domain` value is a six-digit SDBG code. The first three digits identify the top-level domain; the last three identify the subdomain. Top-level domain numbers are the same as in Louw & Nida: `089` in SDBG corresponds to domain 89 ("Relations") in L&N.

SDBG uses numeric subdomains where L&N uses letters. The mapping is positional (A=1, B=2, C=3, ...): `089007` is subdomain 89G in L&N ("Cause and/or Reason"). Domain labels are in `marble-domain-label-mapping.json`.

Note: there is no direct relationship between a subdomain number/letter and the right-hand part of an entry number. Domain 89.32 is within subdomain `089007` (89G), but the 32 does not indicate position within the subdomain — each subdomain contains a set of entries with independent numbering.

### Louw & Nida entry numbers

The `@ln` value is the entry number in Louw & Nida. Multiple lemmas may share an entry (they convey the same sense). For example, LN 89.32 covers ἐπεί, ἐπειδή, and ἐπειδήπερ, all meaning "because, since, for, inasmuch as."

## Source files

| File | Contents |
|------|---------|
| `sdbg-senses.xml` | Per-word-occurrence SDBG sense assignments |
| `sdbg-domains-glosses.xml` | SDBG domain codes with L&N entry numbers and glosses, keyed by MARBLE morphology ID |
| `marble-domain-label-mapping.json` | Human-readable labels for all SDBG domain and subdomain codes |
| `MARBLE-macula-domains-ln.xml` | Mapping between MARBLE IDs and macula word IDs with domain/LN values |

## Credit and license

Word sense and semantic domain data from the United Bible Societies [MARBLE](https://semanticdictionary.org/) project, based on Louw & Nida's *Greek-English Lexicon of the New Testament: Based on Semantic Domains*. Used with permission.

> Johannes P. Louw and Eugene Albert Nida, *Greek-English Lexicon of the New Testament: Based on Semantic Domains* (New York: United Bible Societies, 1996).
