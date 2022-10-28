# macula-greek
## Syntax trees, morphology, and linguistic annotations for the Greek New Testament

This repository contains the MACULA linguistic datasets for the Greek New Testament, including data from:

1. [Nestle1904](https://github.com/biblicalhumanities/Nestle1904) Greek New Testament, edited by Eberhard Nestle, published in 1904 by the British and Foreign Bible Society. Transcription by Diego Santos, morphology by Ulrik Sandborg-Petersen, markup by Jonathan Robie. 
2. Syntax trees developed by Clear Bible, Inc.
3. Glosses from the Berean Study Bible
4. Word sense data from the United Bible Societies [MARBLE](https://semanticdictionary.org/) project, based on Louw & Nida's semantic domains.
5. Semantic roles: Who does what to whom? (Agent, Verb, Patient …)
6. Participant referents: Who is “he,” “she,” or “it” in this sentence?

We are adding further datasets, one at a time. 

This data has been combined into a single set of trees.  There are three variants of this data, found in the following directories:

1. `nodes` contains this data in a set of nested `Node` elements suitable for many NLP systems and other systems that use recursive algorithms.
2. `lowfat` contains the same data in a form more suitable for some kinds of query systems and some kinds of display.  
3. `TSV` contains the word-level data in a TSV table, without syntactic tree structure.  This is simpler for many programs that do not need the complexity of graph structures.

Copyright statements for the individual sources can be found in [the MACULA Greek license](LICENSE.md).
