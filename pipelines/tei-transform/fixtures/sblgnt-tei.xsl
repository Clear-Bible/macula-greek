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

  <xsl:template match="chapter">
      <xsl:copy-of select="."/>
  </xsl:template>

  <xsl:template match="verse-number">
    <!-- FIXME: continuation="true" hack -->
    <xsl:variable name="valid-verse" select="py:usfm_ref(.)" />
    <xsl:if test="$valid-verse">
      <milestone unit="verse">
        <xsl:attribute name="ref">
          <xsl:value-of select="$valid-verse" />
        </xsl:attribute>
      </milestone>
    </xsl:if>
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
      <xsl:for-each select="py:regroup_elements_to_chapters(.)">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
      </xsl:for-each>
    </div>

  </xsl:template>

  <xsl:template match="p[not(node())]"/>

  <xsl:strip-space elements="*"/>
</xsl:stylesheet>
