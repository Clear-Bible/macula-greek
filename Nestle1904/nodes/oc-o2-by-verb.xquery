xquery version "3.1";

(:~
  oc-o2-by-verb.xquery

  For every OC (object complement) and O2 (genuine second object) in the
  Nestle1904 nodes, identify the governing verb, then group and count by
  verb lemma.

  Structure exploited:
    - Every OC / O2 node is a direct child of a Cat="CL" clause node.
    - That clause always has a sibling Cat="V" child that contains the
      governing verb leaf (Cat="verb" with @UnicodeLemma).

  Sort order:
    1. Number of O2 instances ascending  (0 = only-OC verbs first)
    2. Total frequency (OC + O2) descending  (most common verbs within
       each O2-count group appear first)
    3. Lemma ascending  (tie-break)

  Run from this directory in BaseX:
    basex oc-o2-by-verb.xquery
  or load the Nestle1904/nodes collection in BaseX and run:
    basex -i . oc-o2-by-verb.xquery
:)

let $nodes := collection('.')

for $item in $nodes//Node[@Cat = ('OC', 'O2')]
let $verb-leaf := ($item/../Node[@Cat = 'V']//Node[@Cat = 'verb'])[1]
let $lemma     := string($verb-leaf/@UnicodeLemma)
where $lemma != ''
group by $lemma
let $oc    := count($item[@Cat = 'OC'])
let $o2    := count($item[@Cat = 'O2'])
let $total := $oc + $o2
order by $o2 ascending, $total descending, $lemma ascending
return
  <verb lemma="{$lemma}" OC="{$oc}" O2="{$o2}" total="{$total}"/>
