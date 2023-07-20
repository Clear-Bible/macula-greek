# SBLGNT Syntax Trees

## Sources

Sources are equivalent with sources for the Nestle 1904 edition (N1904) except in the following cases:

* SBL Greek New Testament (SBLGNT) from Logos: https://github.com/LogosBible/SBLGNT 
* Glosses (`English` and `Chinese` attributes) from Cherith Analytics
* Word Mapping between N1904 and SBLGNT: https://github.com/Clear-Bible/macula-greek/tree/sblgnt-trees/sources/Clear/mappings 


## Process

Clear Bible produced an edition of syntax trees for the SBLGNT years ago. This MACULA Greek edition
was created by migrating word-level node information from the N1904 MACULA Greek edition into the
SBLGNT where words could be mapped between edition. In these cases, where the SBLGNT analysis did
not already contain information (e.g. `FormalTag` attribute), that information was imported. Where
the SBLGNT already contained information, it was persisted.

Where necessary data (to mirror the N1904) was required, it was created from the SBLGNT as available.
For example, the SBLGNT encoded punctuation in a `Punc` attribute, but the N1904 encodes punctuation
within the text of the word node element. In this case, the SBLGNT `Punc` attribute was used to create
the data necessary to mirror the model provided by N1904.

For cases where the SBLGNT contains readings not present in the N1904, they have been marked as follows:

* `status="unmapped"`: No data available from N1904, data present is from Clear Bible's SBLGNT syntax trees.
* `status="refs-mapped"`: No data available from N1904. However, Clear Bible's SBLGNT syntax trees
had information about pronominal referents (`Ref`), subject referents (`SubjRef`), or Frames (`Frame`)
that had referent identifiers verified and format converted to be compatible with the revised analysis.

The N1904 contains `FunctionalTag` and `FormalTag` attribute information recording word-level
morphological information. This information originates with the [Biblical Humanities edition of the
N1904](https://github.com/biblicalhumanities/Nestle1904/). Morphological data within the Clear Bible
SBLGNT syntax trees was used to reproduce data represented by these attributes for `unmapped` and
`ref-mapped` nodes.

## Future Work

Information in the `Gloss` attribute (reflecting interlinear glosses from the Berean
Interlinear Bible (BIB), [more info](https://github.com/biblicalhumanities/Nestle1904/tree/master/glosses)) 
has only been migrated from the N1904 where nodes have `status="mapped"`. Clear Bible hope to
provide `Gloss` attribute data in the style of the BIB glosses for the remaining 600+ items where `Gloss`
is absent (in the `status="unmapped"` and `status="refs-mapped"` nodes).

