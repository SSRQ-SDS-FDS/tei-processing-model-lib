<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="http://www.w3.org/1999/xhtml" xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:pmf="http://www.tei-c.org/ns/pmf"
                xmlns:xslo="http://www.w3.org/1999/XSL/TransformAlias"
                xpath-default-namespace="http://www.tei-c.org/ns/1.0" version="3.0">
    
    
    <xsl:output indent="yes"/>
    <xsl:import href="behaviour.xsl"/>
    
    <xsl:param name="emit-warning" as="xs:boolean" select="true()"/>
    
    <xsl:namespace-alias stylesheet-prefix="xslo" result-prefix="xsl"/>
 
    <xsl:template match="/">
        <xslo:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                         xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xschema="http://www.w3.org/2001/XMLSchema"
                         xmlns:xs="http://www.w3.org/2001/XMLSchema"
                         exclude-result-prefixes="tei" xpath-default-namespace="http://www.tei-c.org/ns/1.0"
                         version="3.0">
            
            
            <xslo:mode on-no-match="shallow-skip"/>
            
            <xslo:param name="root" select="'//TEI'" as="xs:string"/>
            <xslo:param name="mode" select="'web'" as="xs:string"/>
            
            <xslo:output method="xhtml" omit-xml-declaration="yes"/>

            <xslo:variable name="root-doc" as="element()">
                <xslo:evaluate xpath="$root" as="element()" context-item="."/>
            </xslo:variable>
            
            <xslo:template match="/">
                <xslo:apply-templates select="$root-doc"/>
                <xsl:if test="$emit-warning">
                    <!-- Create warning messages for all elementSpecs without @ident -->
                    <xsl:for-each select="//elementSpec[not(@ident)]">
                        <xslo:message>
                            <xsl:text expand-text="true">WARNING: elementSpec {count(./preceding-sibling::elementSpec) + 1} skipped, because @ident is missing!</xsl:text>
                        </xslo:message>
                    </xsl:for-each>
                </xsl:if>
            </xslo:template>
            
            <xsl:apply-templates select="//elementSpec[.//model][@ident]"/>
            
            <xslo:template match="text()">
                <xslo:value-of select="."/>
            </xslo:template>
            
        </xslo:stylesheet>
    </xsl:template>
    
    <xsl:template match="elementSpec">
        <xsl:apply-templates>
            <xsl:with-param name="el-name" select="@ident" as="xs:string"/>
        </xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="model">
        <xsl:param name="el-name" as="xs:string"/>
        <xslo:template
            match="{$el-name}{string-join(for $i in (@predicate, @output) return '[' || (if ($i/name() != 'output') then $i else '$mode = &quot;' || $i || '&quot;') || ']', '')}">
            <xsl:copy-of select="pmf:create-html-element(.)"/>
        </xslo:template>
    </xsl:template>
    
    
</xsl:stylesheet>
