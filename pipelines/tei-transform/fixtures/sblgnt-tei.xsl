<?xml version="1.0"?>
<xsl:stylesheet
  version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:py="urn:python-funcs"
  exclude-result-prefixes="py"
  >
  <xsl:output
    method="xml"
    indent="yes"
    xml:space="default"
    />

  <xsl:template match="verse-number">
    <milestone unit="verse">
      <xsl:attribute name="ref">
        <xsl:value-of select="py:usfm_ref(.)" />
      </xsl:attribute>
    </milestone>
  </xsl:template>

  <xsl:template match="w">
    <xsl:copy-of select="py:word_transform(.)" />
  </xsl:template>

  <xsl:template match="suffix[not(node())]"/>

  <xsl:template match="suffix">
      <pc type="suffix">
        <xsl:value-of select="translate(., ' ', '')" />
      </pc>
  </xsl:template>

  <xsl:template match="prefix">
      <pc type="prefix">
        <xsl:value-of select="translate(., ' ', '')" />
      </pc>
  </xsl:template>

  <xsl:template match="@*|node()">
    <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:key
    name="p-by-chapter"
    match="p"
    use="substring-before(substring-after(verse-number/@id, ' '), ':')"
    />

  <xsl:template match="/book">
    <div type="book">
      <xsl:attribute name="ref">
        <xsl:value-of select="py:get_book_usfm_ref(.)"/>
      </xsl:attribute>
      <xsl:attribute name="canonical">
        <xsl:value-of select="'true'"/>
      </xsl:attribute>
      <title>
        <xsl:attribute name="type">
          <xsl:value-of select="'main'"/>
        </xsl:attribute>
        <xsl:value-of select="./title/text()" />
      </title>

      <xsl:apply-templates
        select="p[generate-id() = generate-id(key('p-by-chapter', substring-before(substring-after(verse-number/@id, ' '), ':'))[1])]"
        mode="chapter"
        />

    </div>

  </xsl:template>

  <xsl:template
    match="p"
    mode="chapter"
    >
    <xsl:variable
      name="currentChapter"
      select="substring-before(substring-after(verse-number/@id, ' '), ':')"
      />
    <xsl:variable
      name="currentBook"
      select="py:get_book_usfm_ref(.)"
      />
    <xsl:if test="$currentChapter">
      <chapter ref="{$currentBook} {$currentChapter}">
        <title>
          <xsl:value-of select="$currentChapter" />
        </title>
        <xsl:apply-templates select="key('p-by-chapter', $currentChapter)" />
      </chapter>
    </xsl:if>
  </xsl:template>

  <xsl:template match="chapter[@ref]"/>
  <xsl:strip-space elements="*"/>
</xsl:stylesheet>
