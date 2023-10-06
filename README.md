# macula-greek
## Syntax trees, morphology, and linguistic annotations for the Greek New Testament

This repository contains the MACULA linguistic datasets for the Greek New Testament, including data from:

1. [Nestle1904](https://github.com/biblicalhumanities/Nestle1904) Greek New Testament, edited by Eberhard Nestle, published in 1904 by the British and Foreign Bible Society. Transcription by Diego Santos, morphology by Ulrik Sandborg-Petersen, markup by Jonathan Robie.
2. [SBLGNT](https://github.com/LogosBible/SBLGNT) from Logos Bible Software; specifically, the data including the pericope adulturae [from their commit on July 10, 2023](https://github.com/LogosBible/SBLGNT/commit/736fdc76158950c3d04b949b7e013ca14305145a).
3. **_Syntax trees_** developed by Clear Bible, Inc.
4. **_English glosses_** from the Berean Study Bible
5. **_Word sense data_** from the United Bible Societies [MARBLE](https://semanticdictionary.org/) project, based on Louw & Nida's semantic domains.
6. **_Semantic roles_**: Who does what to whom? (Agent, Verb, Patient …)
7. **_Participant referents_**: Who is “he,” “she,” or “it” in this sentence?

We are adding further datasets, one at a time.

This data has been combined into a single set of trees.  There are three variants of this data, found in the following directories:

1. `tei` contains the New Testament text itself in a format that can easily be formatted for readability.
2. `nodes` contains this data in a set of nested `Node` elements suitable for many NLP systems and other systems that use recursive algorithms.
3. `lowfat` contains the same data in a form more suitable for some kinds of query systems and some kinds of display.
4. `TSV` contains the word-level data in a TSV table, without syntactic tree structure.  This is simpler for many programs that do not need the complexity of graph structures.

Copyright statements for the individual sources can be found in [the MACULA Greek license](LICENSE.md).
