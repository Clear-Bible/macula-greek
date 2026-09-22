# TSV

The query contained in `mappings/greek-lowfat-to-tsv.xq` is used to generate `macula-greek-SBLGNT.tsv`.

It can be ran against BaseX via the following command:

```shell
# assumes macula-greek repository root context
./mappings/generate-tsv.sh SBLGNT
```

The wrapper script exists because two non-obvious flags are required, and omitting
either one fails quietly or confusingly:

- `-O xinclude=true` — `SBLGNT/lowfat/sblgntlowfat.xml` is an XInclude index
  pointing at the 27 per-book files, not a merged corpus. BaseX >= 10 defaults
  `XINCLUDE` to `false`, so without this the query matches no `<w>` and writes a
  file containing nothing but the header row.
- `-Djdk.xml.maxElementDepth=0` (passed via `BASEX_JVM`) — the Luke 3:23-38
  genealogy is a recursive NP-of-NP chain nesting `<wg class="np">` 156 levels
  deep. JDK >= 24 caps element depth at 100 and aborts the parse with
  `JAXP00010006: The element "w" has a depth of "101"`.

The script fails with a non-zero exit code if the result comes back suspiciously
small, so a silent regeneration failure cannot go unnoticed. Pass `all` to
regenerate both the SBLGNT and Nestle1904 TSVs.

The [csv-diff](https://pypi.org/project/csv-diff/) Python library may be useful for diffing TSVs:

```shell
# rename the existing file
mv SBLGNT/tsv/macula-greek-SBLGNT.tsv SBLGNT/tsv/macula-greek-SBLGNT-original.tsv

# regenerate the TSV as instructed above

# install csv-diff
pip3 install csv-diff

# run a diff and summarize output in JSON
csv-diff --key="xml:id" --json SBLGNT/tsv/macula-greek-SBLGNT-original.tsv \
    SBLGNT/tsv/macula-greek-SBLGNT.tsv

# optionally use JQ (https://stedolan.github.io/jq/) to get a list of changed IDs
csv-diff --key="xml:id" --json SBLGNT/tsv/macula-greek-SBLGNT-original.tsv \
    SBLGNT/tsv/macula-greek-SBLGNT.tsv \
    | jq '.changed | .[] .key' -r

# remove macula-greek-SBLGNT-original.tsv
rm SBLGNT/tsv/macula-greek-SBLGNT-original.tsv
```
