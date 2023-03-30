<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns="http://www.w3.org/1999/xhtml"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:pmf="http://www.tei-c.org/ns/pmf" xmlns:xslo="http://www.w3.org/1999/XSL/TransformAlias"
    xmlns:map="http://www.w3.org/2005/xpath-functions/map"
    xmlns:array="http://www.w3.org/2005/xpath-functions/array"
    xpath-default-namespace="http://www.tei-c.org/ns/1.0" exclude-result-prefixes="xs map array"
    version="3.0">

    <!-- Notes on the data-structure used here: 
      Each map entry represents a named behaviour
      The value of each entry is map – where the key is the name of the element, which should be created
      and the content is a sequence of parameter names, that should be taken into account
     -->
    <xsl:variable name="pmf:behaviour" as="map(xs:string, map(xs:string, xs:string+))" select="
            
            map {
                'body': map {'body': 'content'},
                'document': map {'html': 'content'},
                'paragraph': map {'p': 'content'}
            }"/>


    <xsl:function name="pmf:create-html-element" as="node()" visibility="public">
        <xsl:param name="model" as="element()"/>
        <xsl:variable name="behaviour-map" as="map(xs:string, xs:string+)"
            select="map:get($pmf:behaviour, $model/@behaviour)"/>
        <xsl:variable name="name" as="xs:string" select="$behaviour-map => map:keys()"/>
        <xsl:element name="{$name}">
            <xsl:attribute name="class"
                select="(pmf:create-default-css-class($model, $name), $model/@cssClass) => string-join(' ')"/>
            <xslo:apply-templates>
                <xsl:if test="$model/param[@name = 'content'][@value]">
                    <xsl:attribute name="select" select="$model/param[@name = 'content']/@value"/>
                </xsl:if>
            </xslo:apply-templates>
        </xsl:element>
    </xsl:function>

    <xsl:function name="pmf:create-default-css-class" as="xs:string" visibility="public">
        <xsl:param name="model" as="element()"/>
        <xsl:param name="name" as="xs:string"/>
        <xsl:choose>
            <xsl:when test="not($model/parent::modelSequence)">
                <xsl:value-of
                    select="('tei', $name, xs:string($model/preceding-sibling::model => count() + 1)) => string-join('-')"
                />
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="'not-implemented-yet'"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:function>

</xsl:stylesheet>
