declare function local:straight-text($node)
{
    for $n at $i in $node//Node[@UnicodeLemma]
        order by $n/@morphId
    return
        string($n/@Unicode)
};

declare function local:simplify($s)
{
  let $element-name :=
      if ($s/@UnicodeLemma) then "w"
      else "wg"
  return 
      element {$element-name} {
        $s/@xml:id,
        $s/@ref,
        attribute cat {$s/@Cat  }[$s/@Cat],
        attribute rule { $s/@Rule }[$s/@Rule],
        attribute lemma {$s/@UnicodeLemma}[$s/@UnicodeLemma],
        attribute head {$s/@Head}[$s/@Head],
        $s/* ! local:simplify(.),
        $s/text()
      }
};

<wf>
{
for $s in //Sentence
let $root :=  $s/Trees/Tree[1]/Node
return 
    <sentence>
      {
        local:straight-text($root),
        local:simplify($root)
      }
    </sentence>
}
</wf>