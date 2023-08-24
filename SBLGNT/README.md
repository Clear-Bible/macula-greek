# SBLGNT Syntax Trees

## Sources

Sources are equivalent with sources for the Nestle 1904 edition (N1904) except in the following cases:

* SBL Greek New Testament (SBLGNT) from Logos: https://github.com/LogosBible/SBLGNT; specifically the data including the pericope adulturae [from their commit on July 10, 2023](https://github.com/LogosBible/SBLGNT/commit/736fdc76158950c3d04b949b7e013ca14305145a).
* **Cherith Glosses for the Greek New Testament**, by Andi Wu, Copyright (C) 2023 by Cherith Analytics, is licensed under a Creative Commons Attribution 4.0 International License ("CC BY 4.0"). This information is represented in the `English` and `Chinese` attributes.
* Glosses (`Gloss` attribute) from the [Berean Interlinear Bible](https://interlinearbible.com/), which is in the public domain ([licensing terms](https://berean.bible/terms.htm)). The glosses implemented in Macula Greek (N1904) are sourced from the Biblical Humanities edition of N1904 ([information here](https://github.com/biblicalhumanities/Nestle1904/tree/master/glosses)). The Berean Bible and Majority Bible texts are officially placed into the public domain as of April 30, 2023.
* Word Mapping between N1904 and SBLGNT: https://github.com/Clear-Bible/macula-greek/tree/sblgnt-trees/sources/Clear/mappings 


## Process

Clear Bible produced an edition of syntax trees for the SBLGNT when the SBLGNT was originally released
under the SBLGNT license. The SBLGNT license was recently updated to CC-BY-4.0 which makes it a better
platform for building and integrating data and analyses. 

This MACULA Greek edition was created by migrating word-level node information from the N1904 MACULA 
Greek edition into the SBLGNT where words could be mapped between edition. In these cases, where the 
SBLGNT analysis did not already contain information (e.g. `FormalTag` attribute), that information was 
imported. Where the SBLGNT already contained information, it was persisted.

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

The following items are separate tasks that need to be done to fully complete migration to SBLGNT:

For Node elements with `status=”(unmapped|refs-mapped)”`:

* Supply context-aware glosses in `GlossBerean` attribute framed/styled like the N1904 `Gloss` attributes 
(which are from the Berean Interlinear Bible) where the `GlossBerean` attribute is missing in Macula Greek SBLGNT.
* Supply Louw-Nida references where LN attribute is missing
* Supply Domain references (based on LN references) where Domain attribute is missing
