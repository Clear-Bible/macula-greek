# TSV

The query contained in `greek-lowfat-to-tsv.xq` is used to generate `macula-greek-SBLGNT.tsv`.

It can be ran against BaseX via the following command:

```shell
# assumes macula-greek repository root context
mkdir -p SBLGNT/tsv
basex -i SBLGNT/lowfat/sblgntlowfat.xml \
    -o SBLGNT/tsv/macula-greek-SBLGNT.tsv \
    mappings/greek-lowfat-to-tsv.xq
```

The [csv-diff](https://pypi.org/project/csv-diff/) Python library may be useful for diffing TSVs:

```shell
# rename the existing file
mv SBLGNT/tsv/macula-greek-SBLGNT.tsv SBLGNT/tsv/macula-greek-SBLGNT-original.tsv

# run tsv/greek-lowfat-to-tsv.xq as instructed above

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
