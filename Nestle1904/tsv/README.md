# TSV

The query contained in `mappings/greek-lowfat-to-tsv.xq` is used to generate `macula-greek-Nestle1904.tsv`.

It can be ran against BaseX via the following command:

```shell
# assumes macula-greek repository root context
./mappings/generate-tsv.sh Nestle1904
```

The wrapper script exists because two non-obvious flags are required, and omitting
either one fails quietly or confusingly:

- `-O xinclude=true` — `Nestle1904/lowfat/nestle1904lowfat.xml` is an XInclude index
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
mv Nestle1904/tsv/macula-greek-Nestle1904.tsv Nestle1904/tsv/macula-greek-Nestle1904-original.tsv

# regenerate the TSV as instructed above

# install csv-diff
pip3 install csv-diff

# run a diff and summarize output in JSON
csv-diff --key="xml:id" --json Nestle1904/tsv/macula-greek-Nestle1904-original.tsv \
    Nestle1904/tsv/macula-greek-Nestle1904.tsv

# optionally use JQ (https://stedolan.github.io/jq/) to get a list of changed IDs
csv-diff --key="xml:id" --json Nestle1904/tsv/macula-greek-Nestle1904-original.tsv \
    Nestle1904/tsv/macula-greek-Nestle1904.tsv \
    | jq '.changed | .[] .key' -r

# remove macula-greek-Nestle1904-original.tsv
rm Nestle1904/tsv/macula-greek-Nestle1904-original.tsv
```
