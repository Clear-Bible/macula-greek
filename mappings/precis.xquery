declare function local:simplify($s)
{
  element {name($s)} {
    $s/@xml:id,
    $s/@ref,
    $s/@class,
    $s/@role,
    $s/@rule,
    $s/* ! local:simplify(.),
    $s/text()
  }
};

<wf>
{
for $s in //sentence
return 
    <sentence>
      {
        $s/p,
        local:simplify($s/wg)
      }
    </sentence>
}
</wf>