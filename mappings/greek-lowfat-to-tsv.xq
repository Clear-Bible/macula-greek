declare function local:val($v)
{
   ($v,"")[1]
};

declare function local:row($w)
{
  for $name in local:headers()
  return
    if ($name = "text") then local:val($w/text()) ! string(.)
    else local:val($w/@*[name(.) = $name])
};

declare function local:headers()
{
    "xml:id",
    "ref",
    "role",
    "class",
    "type",
    "english",
    "chinese",
    "gloss",
    "text",
    "after",
    "lemma",
    "normalized",
    "strong",
    "morph",
    "person",
    "number",
    "gender",
    "case",
    "tense",
    "voice",
    "mood",
    "degree",
    "domain",
    "ln",
    "frame",
    "subjref",
    "referent"
};

string-join(local:headers(), "	")
,
for $w in //w
order by $w/@xml:id
return string-join((local:row($w)), "	")
