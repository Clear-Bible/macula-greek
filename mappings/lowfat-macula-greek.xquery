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
    $node/@domain,
    $node/@ln,
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

declare function local:oneword($node)
(: If the Node governs a single word, return that word. :)
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
    
    let $first := $node/Node[1]
    let $second := $node/Node[2]
    return
        if ($first[@Rule = 'sub-CL']) then
            <wg>
                {
                    local:attributes($second),
                    $node/@nodeId ! attribute xml:id {.},
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
                        $node/@nodeId ! attribute xml:id {.},
                        <!-- two -->,
                        $first/Node ! local:node(.),
                        $second ! local:node(.)
                    }
                </wg>
            else
                <error>{"Something went wrong.", "First:", $first, "Second:", $second}</error>
};

declare function local:is-worth-preserving($clause)
{
    local:node-type($clause/parent::*) = 'role'
    or $clause/@Rule = 'sub-CL'
    or not($clause/@Rule = ('ClCl', 'ClCl2'))
};

declare function local:clause($node)
(:  This is probably too simple as written - need to do restructuring of clauses based on @rule attributes  :)
{
    if (local:is-worth-preserving($node))
    then
        <wg>
            {
                local:attributes($node),
                $node/@nodeId ! attribute xml:id {.},
                $node/Node ! local:node(.)
            }
        </wg>
    else
        $node/Node ! local:node(.)
};


declare function local:phrase($node)
{
    if (local:oneword($node))
    then
        (local:word(local:oneword($node)))
    else
        <wg>
            {
                local:attributes($node),
                $node/@nodeId ! attribute xml:id {.},
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
        if (local:oneword($node))
        then
            (local:word(local:oneword($node), $role))
        else
            if (count($node/Node) > 1)
            then
                <wg>
                    {
                        $role,
                        $node/@nodeId ! attribute xml:id {.},
                        $node/Node ! local:node(.)
                    }
                </wg>
            else
                <wg>
                    {
                        $role,
                        $node/@nodeId ! attribute xml:id {.},
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
    if ($node/*)
    then
        (element error {$role, $node})
    else
        if (string-length($node) = string-length($node/@Unicode) + 1)
        then
            (: place punctuation in a separate node :)
            (
            <w>
                {
                    $role,
                    $node/@nodeId ! attribute ref {local:USFMId($node/@nodeId)},
                    attribute after {substring($node, string-length($node), 1)},
                    local:attributes($node),
                    substring($node, 1, string-length($node) - 1)
                }
            </w>
            )
        else
            <w>
                {
                    $role,
                    $node/@nodeId ! attribute ref {local:USFMId($node/@nodeId)},
                    local:attributes($node),
                    string($node)
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
                <wg
                    role="cl">{$node/Node ! local:node(.)}</wg>
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