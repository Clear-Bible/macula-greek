<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:macula="http://www.w3.org/"
    exclude-result-prefixes="xs" version="2.0">
    <!-- declare macula namespace -->
    <xsl:namespace-alias stylesheet-prefix="xs" result-prefix="xsl"/>

    <xsl:function name="macula:extractDomainNumbers">
        <xsl:param name="attribute"/>
        <xsl:analyze-string select="$attribute" regex="\d{{6}}">
            <xsl:matching-substring>
                    <xsl:value-of select="."/>
            </xsl:matching-substring>
            <xsl:non-matching-substring/>
        </xsl:analyze-string>
    </xsl:function>
    
    <xsl:function name="macula:extractSDBGNumbers">
        <xsl:param name="attribute"/>
        <xsl:value-of select="tokenize($attribute, ';')[2]"/>
    </xsl:function>

    <xsl:template match="@* | node()">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()"/>
        </xsl:copy>
    </xsl:template>


    <xsl:template match="@Domain">
        <xsl:variable name="Domain" select="macula:extractDomainNumbers(data(.))"/>
        <xsl:attribute name="domain">
            <xsl:value-of select="$Domain"/>
        </xsl:attribute> 
    </xsl:template>
    
    <xsl:template match="@SDBG">
        <xsl:variable name="sdbg" select="macula:extractSDBGNumbers(data(.))"/>
        <xsl:attribute name="ln">
            <xsl:value-of select="$sdbg"/>
        </xsl:attribute> 
    </xsl:template>


</xsl:stylesheet>
