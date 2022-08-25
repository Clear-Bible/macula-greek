(:
    Convert GBI trees to Lowfat format.

	NOTE: this should rarely be used now that the lowfat trees
	are being independently, but I am keeping it in the repo
	for documentation purposes and also for quality assurance,
	as a way of testing the lowfat trees against GBI as we
	move forward.

	If it is used, remember to do the following steps:

	- Search for duplicate IDs, removing the second GBI interpretation when there are duplicate subtrees.
	- Search for the single instance where a word is not in any word group, but directly in a sentence.
	- Do a diff to make sure things make sense.

:)


declare variable $retain-singletons := false();

declare function local:USFMBook($nodeId)
{
if(string-length($nodeId) < 1)
then "error5"
else
    switch (xs:integer(substring($nodeId, 1, 2)))
        case 01 return "GEN"
        case 02 return "EXO"
        case 03 return "LEV"
        case 04 return "NUM"
        case 05 return "DEU"
        case 06 return "JOS"
        case 07 return "JDG"
        case 08 return "RUT"
        case 09 return "1SA"
        case 10 return "2SA"
        case 11 return "1KI"
        case 12 return "2KI"
        case 13 return "1CH"
        case 14 return "2CH"
        case 15 return "EZR"
        case 16 return "NEH"
        case 17 return "EST"
        case 18 return "JOB"
        case 19 return "PSA"
        case 20 return "PRO"
        case 21 return "ECC"
        case 22 return "SNG"
        case 23 return "ISA"
        case 24 return "JER"
        case 25 return "LAM"
        case 26 return "EZK"
        case 27 return "DAN"
        case 28 return "HOS"
        case 29 return "JOL"
        case 30 return "AMO"
        case 31 return "OBA"
        case 32 return "JON"
        case 33 return "MIC"
        case 34 return "NAM"
        case 35 return "HAB"
        case 36 return "ZEP"
        case 37 return "HAG"
        case 38 return "ZEC"
        case 39 return "MAL"
        case 40 return "MAT"
        case 41 return "MRK"
        case 42 return "LUK"
        case 43 return "JHN"
        case 44 return "ACT"
        case 45 return "ROM"
        case 46 return "1CO"
        case 47 return "2CO"
        case 48 return "GAL"
        case 49 return "EPH"
        case 50 return "PHP"
        case 51 return "COL"
        case 52 return "1TH"
        case 53 return "2TH"
        case 54 return "1TI"
        case 55 return "2TI"
        case 56 return "TIT"
        case 57 return "PHM"
        case 58 return "HEB"
        case 59 return "JAS"
        case 60 return "1PE"
        case 61 return "2PE"
        case 62 return "1JN"
        case 63 return "2JN"
        case 64 return "3JN"
        case 65 return "JUD"
        case 66 return "REV"
        default return "###"
};

declare function local:verbal-noun-type($node)
(:  This realy doesn't work yet. Not even close. :)
{
    switch ($node/parent::Node/@Cat)
        case 'adjp'
            return
                attribute type {'adjectival'}
        case 'advp'
            return
                attribute type {'adverbial'}
        case 'np'
            return
                attribute type {'nominal'}
        default return
            attribute type {'?'}
};

declare function local:head($node)
{
    if ($node)
    then
        let $preceding := count($node/preceding-sibling::Node)
        let $following := count($node/following-sibling::Node)
        return
            if ($preceding + $following > 0)
            then
                if ($preceding = $node/parent::*/@Head and $node/parent::*/@Cat != 'conj')
                then
                    attribute head {true()}
                else
                    ()
            else
                local:head($node/parent::*)
    else
        ()

};

declare function local:attributes($node)
{
    $node/@Cat ! attribute class {lower-case(.)},
    $node/@Type ! attribute type {lower-case(.)}[string-length(.) >= 1 and not(. = ("Logical", "Negative"))],
    $node/@xml:id,
    $node/@HasDet ! attribute articular {true()},
    $node/@UnicodeLemma ! attribute lemma {.},
    $node/@NormalizedForm ! attribute normalized {.},
    $node/@StrongNumber ! attribute strong {.},
    $node/@Number ! attribute number {lower-case(.)},
    $node/@Person ! attribute person {lower-case(.)},
    $node/@Gender ! attribute gender {lower-case(.)},
    $node/@Case ! attribute case {lower-case(.)},
    $node/@Tense ! attribute tense {lower-case(.)},
    $node/@Voice ! attribute voice {lower-case(.)},
    $node/@Mood ! attribute mood {lower-case(.)},
    $node/@Mood[. = ('Participle', 'Infinitive')] ! attribute type {local:verbal-noun-type($node)},
    $node/@Degree ! attribute degree {lower-case(.)},
    local:head($node),
    $node[empty(*)] ! attribute discontinuous {"true"}[$node/following::Node[empty(*)][1]/@morphId lt $node/@morphId],
    $node/@Rule ! attribute rule {.},
    $node/@Gloss ! attribute gloss {.},
    $node/@LexDomain ! attribute domain {.},
    $node/@LN ! attribute ln {.},
    $node/@ClType !attribute cltype {.},
    $node/@FunctionalTag ! attribute morph {.},
    $node/@Unicode !attribute unicode {.},
    $node/@Frame !attribute frame {.},
    $node/@Ref ! attribute referent {.},
    $node/@SubjRef !attribute subjref {.}
};

(: TODO: the USFM id does not need to be computed from the Nodes trees, since USFM ids are now included on verses and words :)
declare function local:USFMId($nodeId)
{
if(string-length($nodeId) < 1) 
then "error6NoIDFoundInNode"
else
    concat(local:USFMBook($nodeId),
    " ",
    xs:integer(substring($nodeId, 3, 3)),
    ":",
    xs:integer(substring($nodeId, 6, 3)),
    "!",
    xs:integer(substring($nodeId, 9, 3))
    )
};


declare function local:USFMVerseId($nodeId)
{
if(string-length($nodeId) < 1) 
then "error7"
else
    concat(local:USFMBook($nodeId),
    " ",
    xs:integer(substring($nodeId, 3, 3)),
    ":",
    xs:integer(substring($nodeId, 6, 3))
    )
};

declare function local:nodeId2xmlId($nodeId)
{
   attribute xml:id { concat("n", $nodeId) }
};

declare function local:oneword($node)
(: If the Node governs a single word, return that word. 

   ### TODO: Consider restoring this.  See https://github.com/Clear-Bible/symphony-team/issues/96
:)
{
    if (count($node/Node) > 1)
    then
        ()
    else
        if ($node/Node)
        then
            local:oneword($node/Node)
        else
            $node
};

declare function local:sub-CL-adjunct($node)
{
    
    
};

declare function local:sub-CL-adjunct-parent($node)
{
(:
    ### TODO:  Rewrite based on what we have learned.
:)   
    let $first := $node/Node[1]
    let $second := $node/Node[2]
    return
        if ($first[@Rule = 'sub-CL']) then
            <wg>
                {
                    local:attributes($second),
                    $node/@nodeId ! local:nodeId2xmlId(.),
                    <!-- one -->,
                    $first ! local:node(.),
                    $second/Node ! local:node(.)
                }
            </wg>
        else
            if ($second[@Rule = 'sub-CL']) then
                <wg>
                    {
                        local:attributes($first),
                        $node/@nodeId ! local:nodeId2xmlId(.),
                        <!-- two -->,
                        $first/Node ! local:node(.),
                        $second ! local:node(.)
                    }
                </wg>
            else
                <error>{"Something went wrong.", "First:", $first, "Second:", $second}</error>
};

declare variable $group-rules := ("CLaCL","CLa2CL", "2CLaCL", "2CLaCLaCL", 
    "Conj12CL", "Conj13CL", "Conj14CL", "Conj3CL", "Conj4CL", "Conj5CL", "Conj6CL",
    "Conj7CL", "CLandClClandClandClandCl", "EitherOr4CL", "EitherOr7CL","aCLaCL", "aCLaCLaCL" );

declare function local:clause($node)
(:  
   #### TODO: Rewrite.  Just rewrite. 
   See https://github.com/Clear-Bible/symphony-team/issues/91  
   #### TODO: Don't forget minor clauses !!!
:)
{
    if ($node/@ClType = "Minor") then
        <wg role="aux" class="minor">
         {
            $node/Node ! local:node(.)
         }
        </wg>
    else if (starts-with($node/@Rule, "ClClCl")
     or $node/@Rule = $group-rules
    )then
        <wg role="g" class="g">
         {
            $node/@nodeId ! local:nodeId2xmlId(.),
            $node/@Rule ! attribute rule { lower-case(.) },
            $node/Node ! local:node(.)
         }
        </wg>
    else if ($node/@Rule="ClCl") then
        <wg>
         {
            let $first := $node/*[1]
            let $second := $node/*[2]
            return (
                local:attributes($first),
                $first/@nodeId ! local:nodeId2xmlId(.),
                attribute rewrite { string-join(($node/@Rule, $first/@Rule, $second/@Rule),"!")},
                $first/* ! local:node(.),
                <wg>
                  {
                     attribute class {"n-cl"},
                     local:attributes($second)[name(.) ne "class"],
                     $second/* ! local:node(.)
                  }
                 </wg>
               
            )
          }
          </wg>       
    else if ($node/@Rule="ClCl2") then
        <wg>
         {
            let $first := $node/*[1]
            let $second := $node/*[2]
            return (
                local:attributes($second),
                $second/@nodeId ! local:nodeId2xmlId(.),
                attribute rewrite { string-join(($node/@Rule, $first/@Rule, $second/@Rule),"!")},
                <wg>
                  {
                     attribute class {"n-cl"},
                     local:attributes($first)[name(.) ne "class"],
                     $first/* ! local:node(.)
                  }
                 </wg>
                 ,
                $second/* ! local:node(.)
            )
          }
          </wg>
          (: 
    else if ($node/@Rule="CLandCL2") then
        <wg>
         {
            let $first := $node/*[1]
            let $second := $node/*[2]
            let $third := $node/*[3]
            return (
                local:attributes($third),
                $third/@nodeId ! local:nodeId2xmlId(.),
                attribute rewrite { string-join(($node/@Rule, $first/@Rule, $second/@Rule, $third/@Rule),"!")},
                $first/* ! local:node(.),
                $second ! local:node(.),
                $third/* ! local:node(.)
            )
           }
         </wg>
         :)
    else
        <wg>
         {
            local:attributes($node),
            $node/@nodeId ! local:nodeId2xmlId(.),
            $node/Node ! local:node(.)
         }
        </wg>
};


declare function local:phrase($node)
(:
   ### TODO: Get rid of conditional logic.  That just might be all we need.
:)
{
        <wg>
            {
                local:attributes($node),
                $node/@nodeId ! local:nodeId2xmlId(.),
                $node/Node ! local:node(.)
            }
        </wg>
};

declare function local:role($node)
(:
  A role node can have more than one child in some
  corner cases in the GBI trees, e.g. Gal 4:18, where
  an ADV node contains ADV conj ADV.  I imagine this
  occurs only for conjunctions, but I am not sure.
:)
{
    let $role := attribute role {lower-case($node/@Cat)}
    return
        if (count($node/Node) > 1)
        then
            <wg>
                {
                    $role,
                    $node/@nodeId ! local:nodeId2xmlId(.),
                    $node/Node ! local:node(.)
                }
            </wg>
        else
            <wg>
                {
                    $role,
                    $node/@nodeId ! local:nodeId2xmlId(.),
                    local:attributes($node/Node),
                    $node/Node/Node ! local:node(.)
                }
            </wg>
};

declare function local:word($node)
{
    local:word($node, ())
};

declare function local:word($node, $role)
(: $role can contain a role attribute or a null sequence :)
{
let $wordContent := $node/text()
let $wordContentWithoutBrackets := replace($node/text(), '([\(\)\[\]])', '')
let $normalizedFormWordLength := string-length($node/@NormalizedForm)
let $normalizedFormWithPunctuationLength := $normalizedFormWordLength + 1
return
    if ($node/*)
    then
        (element error {$role, $node})
    else
        if (string-length($wordContentWithoutBrackets) = $normalizedFormWithPunctuationLength)
        then
            (: place punctuation in an 'after' attribute :)
            (
            <w>
                {
                    $role,
                    attribute ref {local:USFMId($node/@nodeId)},
                    attribute after {substring($wordContentWithoutBrackets, string-length($wordContentWithoutBrackets), 1)},
                    local:attributes($node),
                    substring($wordContentWithoutBrackets, 1, string-length($wordContentWithoutBrackets) - 1)
                }


            </w>
            )
        else
            <w>
                {
                    $role,
                    attribute ref {local:USFMId($node/@nodeId)},
                    attribute after {' '},
                    local:attributes($node),
                    string($wordContentWithoutBrackets)
                }
            </w>
};

declare function local:node-type($node as element(Node))
{
    if ($node/@UnicodeLemma)
    then
        "word"
    else
        switch ($node/@Cat)
            case "adj"
            case "adv"
            case "conj"
            case "det"
            case "noun"
            case "num"
            case "prep"
            case "ptcl"
            case "pron"
            case "verb"
            case "intj"
            case "adjp"
            case "advp"
            case "np"
            case "nump"
            case "pp"
            case "vp"
                return
                    "phrase"
            case "S"
            case "IO"
            case "ADV"
            case "O"
            case "O2"
            case "P"
            case "V"
            case "VC"
                return
                    "role"
            case "CL"
                return
                    "clause"
            default
            return
                "####"
};

declare function local:node($node as element(Node))
{
    switch (local:node-type($node))
        case "word"
            return
                local:word($node)
        case "phrase"
            return
                local:phrase($node)
        case "role"
            return
                local:role($node)
        case "clause"
            return
                local:clause($node)
        default
        return
            $node
};

declare function local:straight-text($node)
{
    for $n at $i in $node//Node[local:node-type(.) = 'word']
        order by $n/@morphId
    return
        string($n/@Unicode)
};

declare function local:sentence($node)
{
    <sentence>
        {
            <p>
                {
                    for $verse in distinct-values($node//Node/@nodeId ! local:USFMVerseId(.))
                    return
                        (
                        <milestone
                            unit="verse">
                            {attribute id {$verse}, $verse}
                        </milestone>
                        ,
                        " "
                        )
                }
                {local:straight-text($node)}
            </p>,
            
            if (count($node/Node) > 1 or not($node/Node/@node = 'CL'))
            then
                <wg>{$node/Node ! local:node(.)}</wg>
            else
                local:node($node/Node)
            
        }
    </sentence>
};

processing-instruction xml-stylesheet {'href="treedown.css"'},
processing-instruction xml-stylesheet {'href="boxwood.css"'},
<book>
    {
        attribute id {local:USFMBook((//Node)[1]/@nodeId)},
        (:
            If a sentence has multiple interpretations, Sentence/Trees may contain
            multiple Tree nodes.  We want only the first.
        :)
        for $sentence in //Tree[1]/Node
        return
            local:sentence($sentence)
    }
</book>