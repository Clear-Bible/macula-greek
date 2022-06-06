<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:macula="http://clear.bible"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:template match="@* | node()">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:function name="macula:book-to-number" as="xs:numeric">
        <xsl:param name="book" />
        <xsl:choose>
            <xsl:when test="$book = 'GEN'">
                <xsl:value-of select="01"/>
            </xsl:when>
            <xsl:when test="$book = 'EXO'">
                <xsl:value-of select="02"/>
            </xsl:when>
            <xsl:when test="$book = 'LEV'">
                <xsl:value-of select="03"/>
            </xsl:when>
            <xsl:when test="$book = 'NUM'">
                <xsl:value-of select="04"/>
            </xsl:when>
            <xsl:when test="$book = 'DEU'">
                <xsl:value-of select="05"/>
            </xsl:when>
            <xsl:when test="$book = 'JOS'">
                <xsl:value-of select="06"/>
            </xsl:when>
            <xsl:when test="$book = 'JDG'">
                <xsl:value-of select="07"/>
            </xsl:when>
            <xsl:when test="$book = 'RUT'">
                <xsl:value-of select="08"/>
            </xsl:when>
            <xsl:when test="$book = '1SA'">
                <xsl:value-of select="09"/>
            </xsl:when>
            <xsl:when test="$book = '2SA'">
                <xsl:value-of select="10"/>
            </xsl:when>
            <xsl:when test="$book = '1KI'">
                <xsl:value-of select="11"/>
            </xsl:when>
            <xsl:when test="$book = '2KI'">
                <xsl:value-of select="12"/>
            </xsl:when>
            <xsl:when test="$book = '1CH'">
                <xsl:value-of select="13"/>
            </xsl:when>
            <xsl:when test="$book = '2CH'">
                <xsl:value-of select="14"/>
            </xsl:when>
            <xsl:when test="$book = 'EZR'">
                <xsl:value-of select="15"/>
            </xsl:when>
            <xsl:when test="$book = 'NEH'">
                <xsl:value-of select="16"/>
            </xsl:when>
            <xsl:when test="$book = 'EST'">
                <xsl:value-of select="17"/>
            </xsl:when>
            <xsl:when test="$book = 'JOB'">
                <xsl:value-of select="18"/>
            </xsl:when>
            <xsl:when test="$book = 'PSA'">
                <xsl:value-of select="19"/>
            </xsl:when>
            <xsl:when test="$book = 'PRO'">
                <xsl:value-of select="20"/>
            </xsl:when>
            <xsl:when test="$book = 'ECC'">
                <xsl:value-of select="21"/>
            </xsl:when>
            <xsl:when test="$book = 'SNG'">
                <xsl:value-of select="22"/>
            </xsl:when>
            <xsl:when test="$book = 'ISA'">
                <xsl:value-of select="23"/>
            </xsl:when>
            <xsl:when test="$book = 'JER'">
                <xsl:value-of select="24"/>
            </xsl:when>
            <xsl:when test="$book = 'LAM'">
                <xsl:value-of select="25"/>
            </xsl:when>
            <xsl:when test="$book = 'EZK'">
                <xsl:value-of select="26"/>
            </xsl:when>
            <xsl:when test="$book = 'DAN'">
                <xsl:value-of select="27"/>
            </xsl:when>
            <xsl:when test="$book = 'HOS'">
                <xsl:value-of select="28"/>
            </xsl:when>
            <xsl:when test="$book = 'JOL'">
                <xsl:value-of select="29"/>
            </xsl:when>
            <xsl:when test="$book = 'AMO'">
                <xsl:value-of select="30"/>
            </xsl:when>
            <xsl:when test="$book = 'OBA'">
                <xsl:value-of select="31"/>
            </xsl:when>
            <xsl:when test="$book = 'JON'">
                <xsl:value-of select="32"/>
            </xsl:when>
            <xsl:when test="$book = 'MIC'">
                <xsl:value-of select="33"/>
            </xsl:when>
            <xsl:when test="$book = 'NAM'">
                <xsl:value-of select="34"/>
            </xsl:when>
            <xsl:when test="$book = 'HAB'">
                <xsl:value-of select="35"/>
            </xsl:when>
            <xsl:when test="$book = 'ZEP'">
                <xsl:value-of select="36"/>
            </xsl:when>
            <xsl:when test="$book = 'HAG'">
                <xsl:value-of select="37"/>
            </xsl:when>
            <xsl:when test="$book = 'ZEC'">
                <xsl:value-of select="38"/>
            </xsl:when>
            <xsl:when test="$book = 'MAL'">
                <xsl:value-of select="39"/>
            </xsl:when>
            <xsl:when test="$book = 'MAT'">
                <xsl:value-of select="40"/>
            </xsl:when>
            <xsl:when test="$book = 'MRK'">
                <xsl:value-of select="41"/>
            </xsl:when>
            <xsl:when test="$book = 'LUK'">
                <xsl:value-of select="42"/>
            </xsl:when>
            <xsl:when test="$book = 'JHN'">
                <xsl:value-of select="43"/>
            </xsl:when>
            <xsl:when test="$book = 'ACT'">
                <xsl:value-of select="44"/>
            </xsl:when>
            <xsl:when test="$book = 'ROM'">
                <xsl:value-of select="45"/>
            </xsl:when>
            <xsl:when test="$book = '1CO'">
                <xsl:value-of select="46"/>
            </xsl:when>
            <xsl:when test="$book = '2CO'">
                <xsl:value-of select="47"/>
            </xsl:when>
            <xsl:when test="$book = 'GAL'">
                <xsl:value-of select="48"/>
            </xsl:when>
            <xsl:when test="$book = 'EPH'">
                <xsl:value-of select="49"/>
            </xsl:when>
            <xsl:when test="$book = 'PHP'">
                <xsl:value-of select="50"/>
            </xsl:when>
            <xsl:when test="$book = 'COL'">
                <xsl:value-of select="51"/>
            </xsl:when>
            <xsl:when test="$book = '1TH'">
                <xsl:value-of select="52"/>
            </xsl:when>
            <xsl:when test="$book = '2TH'">
                <xsl:value-of select="53"/>
            </xsl:when>
            <xsl:when test="$book = '1TI'">
                <xsl:value-of select="54"/>
            </xsl:when>
            <xsl:when test="$book = '2TI'">
                <xsl:value-of select="55"/>
            </xsl:when>
            <xsl:when test="$book = 'TIT'">
                <xsl:value-of select="56"/>
            </xsl:when>
            <xsl:when test="$book = 'PHM'">
                <xsl:value-of select="57"/>
            </xsl:when>
            <xsl:when test="$book = 'HEB'">
                <xsl:value-of select="58"/>
            </xsl:when>
            <xsl:when test="$book = 'JAS'">
                <xsl:value-of select="59"/>
            </xsl:when>
            <xsl:when test="$book = '1PE'">
                <xsl:value-of select="60"/>
            </xsl:when>
            <xsl:when test="$book = '2PE'">
                <xsl:value-of select="61"/>
            </xsl:when>
            <xsl:when test="$book = '1JN'">
                <xsl:value-of select="62"/>
            </xsl:when>
            <xsl:when test="$book = '2JN'">
                <xsl:value-of select="63"/>
            </xsl:when>
            <xsl:when test="$book = '3JN'">
                <xsl:value-of select="64"/>
            </xsl:when>
            <xsl:when test="$book = 'JUD'">
                <xsl:value-of select="65"/>
            </xsl:when>
            <xsl:when test="$book = 'REV'">
                <xsl:value-of select="66"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="'99'"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:function>
    
    <xsl:function name="macula:usfm-id-to-n" as="xs:string">
        <xsl:param name="usfmId" as="xs:string"/>
        <xsl:variable name="bookNumber" select="data(macula:book-to-number(tokenize($usfmId, '[.|!|:| ]')[1]))"/>
        <xsl:variable name="chapterNumber" select="tokenize($usfmId, '[.|!|:| ]')[2]"/>
        <xsl:variable name="verseNumber" select="tokenize($usfmId, '[.|!|:| ]')[3]"/>
        <xsl:variable name="wordNumber" select="tokenize($usfmId, '[.|!|:| ]')[4]"/>
        
        <xsl:value-of>
            <xsl:number value="$bookNumber" format="00"/>
            <xsl:number value="$chapterNumber" format="000"/>
            <xsl:number value="$verseNumber" format="000"/>
            <xsl:number value="$wordNumber" format="000"/>
        </xsl:value-of>
    </xsl:function>
    
    <xsl:template match="@ref[parent::w]">
        
        <xsl:variable name="bookNumber" select="macula:book-to-number(.)"/>       
        <xsl:attribute name="xml:id">
            <xsl:choose>
                <xsl:when test="$bookNumber > 39">
                    <!-- 'n' prefix for NT books -->
                    <xsl:value-of select="concat('n', macula:usfm-id-to-n(.))"/>
                </xsl:when>
                <xsl:when test="$bookNumber &lt; 40">
                    <!-- 'o' prefix for OT books -->
                    <xsl:value-of select="concat('o', macula:usfm-id-to-n(.))"/>
                </xsl:when>
                <!-- TEST FOR LXX BOOKS?
                    <xsl:when test=""> 
                        <!-/- 'l' prefix for LXX books -/->
                        <xsl:value-of select="concat('o', macula:usfm-id-to-n(.))"/>
                    </xsl:when>
                -->
                <!-- TEST FOR VULGATE BOOKS? etc.
                    <xsl:when test=""> 
                        <!-/- 'v' prefix for Vulgate books -/->
                        <xsl:value-of select="concat('o', macula:usfm-id-to-n(.))"/>
                    </xsl:when>
                -->
                <xsl:otherwise>ERROR-GENERATING-XMLID</xsl:otherwise>
            </xsl:choose>
        </xsl:attribute>
        <xsl:copy/>
    </xsl:template>
    
    <xsl:function name="macula:node-book-number">
        <xsl:param name="nodeBookId"/>
        <xsl:if test="string-length($nodeBookId) > 0">
            <xsl:value-of select="substring($nodeBookId, 1, 2)"/>
        </xsl:if>
    </xsl:function>
    
    <xsl:template match="@n">
        <xsl:variable name="bookNumber" select="macula:node-book-number(.)"/>
        <xsl:attribute name="xml:id">
            <xsl:choose>
                <xsl:when test="$bookNumber > 39">
                    <!-- 'n' prefix for NT books -->
                    <xsl:value-of select="concat('n', .)"/>
                </xsl:when>
                <xsl:when test="$bookNumber &lt; 40">
                    <!-- 'o' prefix for OT books -->
                    <xsl:value-of select="concat('o', .)"/>
                </xsl:when>
                <!-- TEST FOR LXX BOOKS?
                    <xsl:when test=""> 
                        <!-/- 'l' prefix for LXX books -/->
                        <xsl:value-of select="concat('o', macula:usfm-id-to-n(.))"/>
                    </xsl:when>
                -->
                <!-- TEST FOR VULGATE BOOKS? etc.
                    <xsl:when test=""> 
                        <!-/- 'v' prefix for Vulgate books -/->
                        <xsl:value-of select="concat('o', macula:usfm-id-to-n(.))"/>
                    </xsl:when>
                -->
                <xsl:otherwise>ERROR-GENERATING-XMLID</xsl:otherwise>
            </xsl:choose>
        </xsl:attribute>
    </xsl:template>
</xsl:stylesheet>