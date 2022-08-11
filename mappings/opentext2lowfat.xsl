<?xml version="1.0" encoding="UTF-8"?>

<!-- This stylesheet was produced by Christopher D. Land. It transforms the current OpenText.org annotations into HTML. -->
<xsl:stylesheet xmlns:local="http://clear.bible" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" version="3.1">
    <xsl:output method="xml" indent="yes"/>
    <xsl:strip-space elements="*"/>
    <xsl:variable name="unit_wg" as="xs:string*" select="'text', 'quot', 'turn', 'act', 'move', 'pred', 'event', 'icoll', 'ecoll', 'num'"/>
    <xsl:variable name="name_wg" as="xs:string*" select="'#positional_association'"/>
    <xsl:template match="/"><xsl:processing-instruction name="xml-stylesheet">href="treedown.css"</xsl:processing-instruction><xsl:processing-instruction name="xml-stylesheet">href="boxwood.css"</xsl:processing-instruction><xsl:apply-templates/></xsl:template>
    
    <xsl:function name="local:osis-to-usfm">
        <xsl:param name="osisId" as="xs:string"/>
        <xsl:if test="string-length($osisId) > 0">
            <xsl:variable name="corpus" select="substring($osisId, 1, 6)"/>    
            <xsl:variable name="nonCorpus" select="tokenize(substring($osisId, 7), '\.')"/>
            <xsl:variable name="book" select="upper-case($nonCorpus[1])"/>
            <xsl:variable name="chapter" select="$nonCorpus[2]"/>
            <xsl:variable name="verse" select="$nonCorpus[3]"/>
            <xsl:variable name="word" select="$nonCorpus[4]"/>
            <xsl:value-of select="$book || ' ' || $chapter || ':' || $verse || '!' || $word"/>
        </xsl:if>
    </xsl:function>
    
    <xsl:template match="OpenText">
        <xsl:apply-templates select="node()"/>
    </xsl:template>
    
    <xsl:template match="text">
        <xsl:variable name="bookId">
            <xsl:value-of select="substring-before(local:osis-to-usfm(@xml:id), ' ')"/>
        </xsl:variable>
        <book id="">
            <xsl:attribute name="id" select="$bookId"/>
            <xsl:apply-templates select="node()"/>
        </book>
    </xsl:template>
    
    <xsl:template match="header">
        <!--<xsl:copy-of select="."/>-->
    </xsl:template>
    <xsl:template match="e[@type = 'adj']">
        <xsl:apply-templates>
            <xsl:with-param name="head" tunnel="yes" as="xs:boolean" select="false()"/>
        </xsl:apply-templates>
    </xsl:template>
    <xsl:template match="e[@type = 'mark']">
        <xsl:apply-templates>
            <xsl:with-param name="head" tunnel="yes" as="xs:boolean" select="false()"/>
            <xsl:with-param name="role" tunnel="yes" as="xs:string?" select="()"/>
        </xsl:apply-templates>
    </xsl:template>
    <!-- This handles most of the grammatical nodes. -->
    <xsl:template match="m | p | w | e[@type = 'tok']">
        <xsl:param name="passed-role" tunnel="yes" as="xs:string?"/>
        <xsl:param name="passed-class" tunnel="yes" as="xs:string?"/>
        <xsl:param name="head" tunnel="yes" as="xs:boolean" select="false()"/>
        <xsl:variable name="path" as="xs:string?" select="
            if (self::p) then
            @n
            else
            ()"/>
        <xsl:variable name="role" as="xs:string?">
            <xsl:choose>
                <xsl:when test="ancestor::e[1][@type = 'mark']"/>
                <xsl:when test="@name = 'addressing'">~</xsl:when> <!-- Should be 'voc' -->
                <xsl:when test="@name = 'interjecting'">~</xsl:when> <!-- Should be 'intj' -->
                <xsl:when test="@name = 'introducing'">~</xsl:when> <!-- Should be 'topic' or something -->
                <xsl:when test="@name = 'instantiator_construal'">s</xsl:when>
                <xsl:when test="@name = 'objectifying'">o</xsl:when>
                <xsl:when test="@name = 'extra_participant'">o2</xsl:when>
                <xsl:when test="@name = 'complementary_instantiation'">vc</xsl:when>
                <xsl:when test="@name = 'circumstance'">adv</xsl:when>
                <xsl:when test="@name = 'elaborated'"></xsl:when> <!-- Should be 'mod' or 'modifier' -->
                <xsl:when test="@name = '#relative_differentiation'">adv</xsl:when>
                
                <xsl:when test="$passed-role">
                    <xsl:value-of select="$passed-role"/>
                </xsl:when>
                <xsl:when test="$passed-class = 'cl'">pred</xsl:when>
                <xsl:when test="$passed-class = 'vp'">v</xsl:when>
                <xsl:when test="$passed-class = 'np'"></xsl:when> <!-- Should be something like 'subst' or 'nominal' -->
                <xsl:when test="$passed-class = ('adjp', 'advp', 'nump')"></xsl:when> <!-- Could be 'head' -->
            </xsl:choose>
        </xsl:variable>
        <xsl:variable name="class" as="xs:string?">
            <xsl:choose>
                <xsl:when test="@unit = ('text', 'quot', 'turn', 'act')"/>
                <!--<xsl:value-of select="@unit"/>-->
                <!--</xsl:when>-->
                <xsl:when test="@unit = 'move'">sentence</xsl:when>
                <xsl:when test="@unit = 'pred'">cl</xsl:when>
                <xsl:when test="@unit = 'event'">vp</xsl:when>
                <xsl:when test="@unit = 'def' and m[@name = '!extrinsic']/m[@name = '!derived_definition']">np</xsl:when>
                <xsl:when test="@unit = 'icoll' and not(ancestor::w[1]/m[@name = '#mannerism'])">adjp</xsl:when>
                <xsl:when test="@unit = 'ecoll'">advp</xsl:when>
                <xsl:when test="@unit = 'num'">nump</xsl:when>
                <xsl:when test="@name = 'sequence'">coordination-group</xsl:when>
                <xsl:when test="@name = 'junction'">junc</xsl:when>
                <xsl:when test="@name = 'apposition'">appos</xsl:when>
                <xsl:when test="@name = 'operation'">oper</xsl:when>
                <xsl:when test="@name = '#positional_association'">p</xsl:when>
                <xsl:when test="@name = '#mannerism'">advp</xsl:when>
                <xsl:when test="@name = '#propositional_association'">sc</xsl:when>
                <xsl:when test="@name = '#proposition'">cc</xsl:when>
                <xsl:when test="@name = '#quotation'">dd</xsl:when>
                <xsl:when test="@name = '#occurrence'">ac</xsl:when>
                <xsl:when test="@name = '#scenario'">ic</xsl:when>
            </xsl:choose>
        </xsl:variable>
        <xsl:choose>
            <xsl:when test="$role = 'pred'">
                <!-- NOTE: ignoring the subject/predicate distinction because it's not in the original lowfat, but it will be very helpful for distinguishing arguments/adjuncts in the future -->
                <xsl:apply-templates>
                    <xsl:with-param name="passed-role" tunnel="yes" as="xs:string?" select="()"/>
                    <xsl:with-param name="passed-class" tunnel="yes" as="xs:string?" select="$class"/>
                    <xsl:with-param name="head" tunnel="yes" as="xs:boolean" select="true()"/>
                </xsl:apply-templates>
            </xsl:when>
            <xsl:when test="$class = 'sentence' and not(./ancestor::w[@unit='quot'])">
                <xsl:variable name="allUsfmRefs" select=".//@xml:id"/>
                <xsl:variable name="tokenizedUsfmRefs">
                        <xsl:for-each select="$allUsfmRefs">
                                    <xsl:value-of select="'+' || tokenize(., '\.')[2] || '.' || tokenize(., '\.')[3] || '.' || tokenize(., '\.')[4]"/>
                            <!--<xsl:choose>
                                <xsl:when test="position() = 1"/>
                                <xsl:otherwise>
                                </xsl:otherwise>
                            </xsl:choose>-->
                        </xsl:for-each>
                </xsl:variable>
                <xsl:variable name="usfmRefs" select="distinct-values(tokenize($tokenizedUsfmRefs, '\+'))"/>
                <sentence>
                    <p>
                        <xsl:for-each select="$usfmRefs">
                            <xsl:sort select="." order="ascending"/> 
                            <xsl:if test=". = ''"/>
                            <xsl:if test="not(. = '')">
                                <xsl:variable name="usfmBook" select="upper-case(tokenize(., '\.')[1])"/>
                                <xsl:variable name="usfmCh" select="tokenize(., '\.')[2]"/>
                                <xsl:variable name="usfmV" select="tokenize(., '\.')[3]"/>
                                <xsl:variable name="refString"><xsl:value-of select="concat($usfmBook, ' ', $usfmCh, ':', $usfmV)"/></xsl:variable>
                                <milestone unit="verse" id="{$refString}"><xsl:value-of select="$refString"/></milestone>                        
                            </xsl:if>
                        </xsl:for-each>
                        <xsl:value-of>
                            <xsl:for-each select=".//e[@type='w']">
                                <xsl:variable name="afterPC" select="./following-sibling::e[@type='pc']"/>
                                <xsl:value-of select="./text() || $afterPC || ' '"/>
                            </xsl:for-each>
                        </xsl:value-of>
                    </p>
                    <wg role="cl">
                        <xsl:apply-templates select="node()"/>
                    </wg>
                </sentence>
            </xsl:when>
            <xsl:when test="$class or $path or count(descendant-or-self::e[@type = 'w']) > 1">
                <xsl:choose>
                    <xsl:when test="$class = 'oper' and count(m[descendant::e[@type = 'tok']]) > 1">
                        <wg>
                            <xsl:attribute name="class" select="$class"/>
                            <xsl:if test="$head">
                                <xsl:attribute name="head" select="'true'"/>
                            </xsl:if>
                            <xsl:apply-templates select="e[@type = 'mark']"/>
                            <wg>
                                <xsl:if test="$role">
                                    <xsl:attribute name="role" select="$role"/>
                                </xsl:if>
                                <xsl:apply-templates select="* except e[@type = 'mark']">
                                    <xsl:with-param name="passed-role" tunnel="yes" as="xs:string?" select="()"/>
                                    <xsl:with-param name="passed-class" tunnel="yes" as="xs:string?" select="$class"/>
                                    <xsl:with-param name="head" tunnel="yes" as="xs:boolean" select="true()"/>
                                </xsl:apply-templates>
                            </wg>
                        </wg>
                    </xsl:when>
                    <xsl:when test="$class or $path">
                        <xsl:if test="$path">
                            <xsl:apply-templates>
                                <xsl:with-param name="passed-role" tunnel="yes" as="xs:string?" select="$role"/>
                                <xsl:with-param name="passed-class" tunnel="yes" as="xs:string?" select="$class"/>
                            </xsl:apply-templates>
                        </xsl:if>
                        <xsl:if test="not($path)">                     
                            <wg>
                                <xsl:if test="$role">
                                    <xsl:attribute name="role" select="$role"/>   
                                </xsl:if>
                                <xsl:if test="$class">
                                    <xsl:choose>
                                        <xsl:when test="$class = 'p'">
                                            <xsl:attribute name="role" select="'adv'"/> <!-- Force prepositional phrases to be '+' -->
                                        </xsl:when>
                                        <xsl:when test="$class = 'sc'">
                                            <xsl:attribute name="role" select="'adv'"/> <!-- Force subord. clauses to be '+' -->
                                        </xsl:when>
                                        <xsl:when test="$class = 'vp'"> <!-- Force verb phrases to be the child m node name or no role -->
                                            <!-- Only use child m name if it does not start with $, which would be the verb -->
                                            <xsl:if test="not(substring(child::m[1]/@name,1,1) = '$')">
                                                <xsl:variable name="vp-role" as="xs:string?">
                                                    <xsl:choose>
                                                        <!--<xsl:when test="ancestor::e[1][@type = 'mark']"/>-->
                                                        <xsl:when test="child::m[1]/@name = 'addressing'">~</xsl:when> <!-- Should be 'voc' -->
                                                        <xsl:when test="child::m[1]/@name = 'interjecting'">~</xsl:when> <!-- Should be 'intj' -->
                                                        <xsl:when test="child::m[1]/@name = 'introducing'">~</xsl:when> <!-- Should be 'topic' or something -->
                                                        <xsl:when test="child::m[1]/@name = 'instantiator_construal'">s</xsl:when>
                                                        <xsl:when test="child::m[1]/@name = 'objectifying'">o</xsl:when>
                                                        <xsl:when test="child::m[1]/@name = 'extra_participant'">o2</xsl:when>
                                                        <xsl:when test="child::m[1]/@name = 'complementary_instantiation'">vc</xsl:when>
                                                        <xsl:when test="child::m[1]/@name = 'circumstance'">adv</xsl:when>
                                                        <xsl:when test="child::m[1]/@name = 'elaborated'"></xsl:when> <!-- Should be 'mod' or 'modifier' -->
                                                        <xsl:when test="child::m[1]/@name = '#relative_differentiation'">adv</xsl:when>
                                                        <xsl:when test="child::m/m[@name = 'complementary_instantiation']">adv</xsl:when>
                                                        <xsl:otherwise>adv</xsl:otherwise> <!-- NOTE: this catches a lot of other things, often coordinated clauses (like protosasis/apodosis, for exapmle) -->
                                                        <!--<xsl:when test="$passed-role">
                                                            <xsl:value-of select="$passed-role"/>
                                                        </xsl:when>
                                                        <xsl:when test="$passed-class = 'cl'">pred</xsl:when>
                                                        <xsl:when test="$passed-class = 'vp'">v</xsl:when>
                                                        <xsl:when test="$passed-class = 'np'"></xsl:when> <!-\- Should be something like 'subst' or 'nominal' -\->
                                                        <xsl:when test="$passed-class = ('adjp', 'advp', 'nump')"></xsl:when> <!-\- Could be 'head' -\->-->
                                                    </xsl:choose>
                                                </xsl:variable>
                                                
                                                <xsl:attribute name="role" select="$vp-role"/>
                                                
                                                <!-- The VP should not be @class='cl' when it is the grandchild of a pred -->
                                                <xsl:choose>
                                                    <xsl:when test="./../../self::w[@unit='pred']"/>
                                                    <xsl:otherwise>
                                                        <xsl:attribute name="class" select="'cl'"/>
                                                    </xsl:otherwise>
                                                </xsl:choose>
                                            </xsl:if>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:attribute name="class" select="$class"/>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:if>
                                <xsl:if test="$head and not($path)">
                                    <xsl:attribute name="head" select="'true'"/>
                                </xsl:if>
                                <xsl:apply-templates>
                                    <xsl:with-param name="passed-role" tunnel="yes" as="xs:string?" select="()"/>
                                    <xsl:with-param name="passed-class" tunnel="yes" as="xs:string?" select="$class"/>
                                    <xsl:with-param name="head" tunnel="yes" as="xs:boolean" select="true()"/>
                                </xsl:apply-templates>
                            </wg>
                        </xsl:if>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:apply-templates>
                            <xsl:with-param name="passed-role" tunnel="yes" as="xs:string?" select="$role"/>
                            <xsl:with-param name="passed-class" tunnel="yes" as="xs:string?" select="
                                if ($class) then
                                $class
                                else
                                $passed-class"/>
                        </xsl:apply-templates>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:when test="@type = 'tok'">
                <w>
                    <xsl:if test="$path">
                        <xsl:attribute name="path" select="$path"/>
                    </xsl:if>
                    <xsl:if test="$role">
                        <xsl:attribute name="role" select="$role"/>
                    </xsl:if>
                    <xsl:attribute name="pos" select="@pos"/>
                    <xsl:if test="$head">
                        <xsl:attribute name="head" select="'true'"/>
                    </xsl:if>                    
                    <!-- Try to match attributes of original lowfat -->
                    
                    <!-- Turn OSIS ref into USFM ref -->
                    <xsl:variable name="usfmRef" select="substring(@xml:id, 7)"/>
                    <xsl:variable name="usfmBook" select="upper-case(tokenize($usfmRef, '\.')[1])"/>
                    <xsl:variable name="usfmCh" select="tokenize($usfmRef, '\.')[2]"/>
                    <xsl:variable name="usfmV" select="tokenize($usfmRef, '\.')[3]"/>
                    <xsl:variable name="usfmW" select="tokenize($usfmRef, '\.')[4]"/>
                    <xsl:variable name="refString"><xsl:value-of select="concat($usfmBook, ' ', $usfmCh, ':', $usfmV, '!', $usfmW)"/></xsl:variable>
                    
                    <xsl:attribute name="ref"><xsl:value-of select="$refString"/></xsl:attribute>
                    
                    <!-- Turn PCs into @after attribute -->
                    <xsl:if test="e[last()][@type = 'pc']">
                        <xsl:attribute name="after" select="string(e[@type = 'w']/following-sibling::e[@type = 'pc'])"/>
                    </xsl:if>
                    <xsl:if test="e[1][@type = 'pc']">
                        <xsl:attribute name="before" select="string(e[@type = 'w']/preceding-sibling::e[@type = 'pc'])"/>
                    </xsl:if>
                    
                    <xsl:copy-of select="@class"/>
                    <xsl:attribute name="type"><xsl:value-of select="@posClass"/></xsl:attribute>
                    
                    <!-- Build matching @xml:id -->
                    <xsl:attribute name="xml:id">
                        <xsl:variable name="corpus">n</xsl:variable>
                        <xsl:variable name="book"> <!-- NOTE: The book number needs to be dynamically calculated -->
                            <xsl:variable name="bookFromXMLId" select="tokenize(@xml:id, '\.')[2]"/>
                            <xsl:choose>
                                <xsl:when test="$bookFromXMLId = 'Gal'">48</xsl:when>
                                <xsl:when test="$bookFromXMLId = '1Thess'">52</xsl:when>
                            </xsl:choose>
                        </xsl:variable> 
                        <xsl:variable name="chapter">
                            <xsl:variable name="chapterFromXMLId" select="tokenize(@xml:id, '\.')[3]"/>
                            <!-- Make sure $chapterFromXMLId is a 3-digit number by adding leading zeros if necessary -->
                            <xsl:value-of>
                                <xsl:number value="number($chapterFromXMLId)" format="001"/>
                            </xsl:value-of>
                        </xsl:variable>
                        <xsl:variable name="verse">
                            <xsl:variable name="verseFromXMLId" select="tokenize(@xml:id, '\.')[4]"/>
                            <!-- Make sure $verseFromXMLId is a 3-digit number by adding leading zeros if necessary -->
                            <xsl:value-of>
                                <xsl:number value="number($verseFromXMLId)" format="001"/>
                            </xsl:value-of>
                        </xsl:variable>
                        <xsl:variable name="word">
                            <xsl:variable name="wordFromXMLId" select="tokenize(@xml:id, '\.')[5]"/>
                            <!-- Make sure $wordFromXMLId is a 3-digit number by adding leading zeros if necessary -->
                            <xsl:value-of>
                                <xsl:number value="number($wordFromXMLId)" format="001"/>
                            </xsl:value-of>
                        </xsl:variable>
                        <xsl:value-of select="$corpus || $book || $chapter || $verse || $word"/>
                    </xsl:attribute>
                    
                    <xsl:copy-of select="@lemma"/>
                    <xsl:attribute name="normalized" select="@norm"/>
                    <xsl:copy-of select="@strong"/>
                    <xsl:copy-of select="@number"/>
                    <xsl:copy-of select="@gender"/>
                    <xsl:copy-of select="@case"/>
                    <xsl:copy-of select="@gloss"/>
                    <xsl:attribute name="domain"><xsl:value-of select="'TBA'"/></xsl:attribute>
                    <xsl:attribute name="ln"><xsl:value-of select="'TBA'"/></xsl:attribute>
                    <xsl:attribute name="morph"><xsl:value-of select="@formal"/></xsl:attribute>
                    <xsl:attribute name="unicode"><xsl:value-of select="@norm"/></xsl:attribute>
                    
                    <!-- Catch any remaining attributes -->
                    <!--<xsl:copy-of select="@* except (@middle | @formal | @functional | @norm | @n)"/>-->
                    
                    <xsl:apply-templates select="e[@type = 'w']"/>
                </w>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates>
                    <xsl:with-param name="passed-role" tunnel="yes" as="xs:string?" select="$role"/>
                    <xsl:with-param name="passed-class" tunnel="yes" as="xs:string?" select="
                        if ($class) then
                        $class
                        else
                        $passed-class"/>
                </xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="/OpenText/text/w/w/m[@name='sequence'][not(./ancestor::m)]">
        <xsl:apply-templates select="node()"/>
    </xsl:template>
    
</xsl:stylesheet>