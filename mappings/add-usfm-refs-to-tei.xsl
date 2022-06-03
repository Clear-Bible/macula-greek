<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    xmlns:macula="http://www.w3.org/"
    version="2.0">
    
    <xsl:template match="@* | node()">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:function name="macula:USFMBook" as="xs:string">
        <xsl:param name="nodeBookId" as="xs:string"/>
        <xsl:if test="string-length($nodeBookId) > 0">
            <xsl:variable name="nodeBookNumber">
                <xsl:value-of select="tokenize($nodeBookId, '[.]')[1]"/>
            </xsl:variable>
            <xsl:choose>
                <xsl:when test="$nodeBookNumber = 'Matt'">
                    <xsl:value-of select="'MAT'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = 'Mark'">
                    <xsl:value-of select="'MRK'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = 'Luke'">
                    <xsl:value-of select="'LUK'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = 'John'">
                    <xsl:value-of select="'JHN'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = 'Acts'">
                    <xsl:value-of select="'ACT'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = 'Rom'">
                    <xsl:value-of select="'ROM'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = '1Cor'">
                    <xsl:value-of select="'1CO'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = '2Cor'">
                    <xsl:value-of select="'2CO'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = 'Gal'">
                    <xsl:value-of select="'GAL'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = 'Eph'">
                    <xsl:value-of select="'EPH'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = 'Phil'">
                    <xsl:value-of select="'PHP'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = 'Col'">
                    <xsl:value-of select="'COL'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = '1Thess'">
                    <xsl:value-of select="'1TH'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = '2Thess'">
                    <xsl:value-of select="'2TH'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = '1Tim'">
                    <xsl:value-of select="'1TI'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = '2Tim'">
                    <xsl:value-of select="'2TI'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = 'Titus'">
                    <xsl:value-of select="'TIT'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = 'Phlm'">
                    <xsl:value-of select="'PHM'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = 'Heb'">
                    <xsl:value-of select="'HEB'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = 'Jas'">
                    <xsl:value-of select="'JAS'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = '1Pet'">
                    <xsl:value-of select="'1PE'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = '2Pet'">
                    <xsl:value-of select="'2PE'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = '1John'">
                    <xsl:value-of select="'1JN'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = '2John'">
                    <xsl:value-of select="'2JN'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = '3John'">
                    <xsl:value-of select="'3JN'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = 'Jude'">
                    <xsl:value-of select="'JUD'"/>
                </xsl:when>
                <xsl:when test="$nodeBookNumber = 'Rev'">
                    <xsl:value-of select="'REV'"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="'###'"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:if>
    </xsl:function>
    
    <xsl:function name="macula:ref">
        <xsl:param name="osisId" as="xs:string"/>
        <xsl:choose>
            <xsl:when test="count(tokenize($osisId, '[.|!]')) = 1">
                <!-- book only -->
                <xsl:variable name="book" select="macula:USFMBook($osisId)"/>
                <xsl:value-of select="$book"/>
            </xsl:when>
            <xsl:when test="count(tokenize($osisId, '[.|!]')) = 2">
                <!-- book and chapter -->
                <xsl:variable name="book" select="macula:USFMBook($osisId)"/>
                <xsl:variable name="chapter" select="tokenize($osisId, '[.|!]')[2]"/>
                <xsl:value-of select="concat($book, ' ', $chapter)"/>
            </xsl:when>
            <xsl:when test="count(tokenize($osisId, '[.|!]')) = 3">
                <!-- book, chapter and verse -->
                <xsl:variable name="book" select="macula:USFMBook($osisId)"/>
                <xsl:variable name="chapter" select="tokenize($osisId, '[.|!]')[2]"/>
                <xsl:variable name="verse" select="tokenize($osisId, '[.|!]')[3]"/>
                <xsl:value-of select="concat($book, ' ', $chapter, ':', $verse)"/>
            </xsl:when>
            <xsl:when test="count(tokenize($osisId, '[.|!]')) = 4">
                <!-- book, chapter, verse, and word -->
                <xsl:variable name="book" select="macula:USFMBook($osisId)"/>
                <xsl:variable name="chapter" select="tokenize($osisId, '[.|!]')[2]"/>
                <xsl:variable name="verse" select="tokenize($osisId, '[.|!]')[3]"/>
                <xsl:variable name="word" select="tokenize($osisId, '[.|!]')[4]"/>
                <xsl:value-of select="concat($book, ' ', $chapter, ':', $verse, '!', $word)"/>
            </xsl:when>
        </xsl:choose>
        
    </xsl:function>
    
    <xsl:template match="@osisId | @id | @osisID">
        <xsl:attribute name="ref">
            <xsl:value-of select="macula:ref(.)"/>
        </xsl:attribute> 
    </xsl:template>
    
</xsl:stylesheet>