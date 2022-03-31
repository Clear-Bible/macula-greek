# macula-greek
## Syntax trees, morphology, and linguistic annotations for the Greek New Testament

This repository contains the MACULA linguistic datasets for the Greek New Testament, including data from:

1. [Nestle1904](https://github.com/biblicalhumanities/Nestle1904) Greek New Testament, edited by Eberhard Nestle, published in 1904 by the British and Foreign Bible Society. Transcription by Diego Santos, morphology by Ulrik Sandborg-Petersen, markup by Jonathan Robie. 
2. Syntax trees developed by Clear Bible, Inc.
3. Word sense data from the United Bible Societies [MARBLE](https://semanticdictionary.org/) project.

During 2022, we intend to add further datasets, which are under development:

5. Synonyms: Which Greek words are related in meaning?
6. Semantic roles: Who does what to whom? (Agent, Verb, Patient …)
7. Participant referents: Who is “he,” “she,” or “it” in this sentence?
8. Semantic similarity: Which phrases and clauses have are semantically similar to texts found elsewhere?

This data has been combined into a single set of trees.  There are two variants of the these trees, found in the following directories:

1. `nodes` contains this data in a set of nested `Node` elements suitable for many NLP systems and other systems that use recursive algorithms.
2. `lowfat` contains the same data in a form more suitable for some kinds of query systems and some kinds of display.

Copyright statements for the individual sources can be found in [the MACULA Greek license](LICENSE.md).
