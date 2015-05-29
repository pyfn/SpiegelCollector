# -*- coding: utf-8 -*-

"""
Namespace for Utility functions to build the article dictionary
"""

from time import mktime, strptime
from bs4 import BeautifulSoup as bs
from re import sub as re_sub

#german_charakters = {'\xf6':'oe','\xd6':'Oe','\xc4':'Ae','\xe4':'ae','\xdc':'Ue','\xfc':'ue','\xdf':'ss','\xa9':'C','\xf3':'o','\xe7':'c','\xa0':' ','\xe1':'a','\xe9':'e','\'':'"','[;:]':'.'
#}

def _makeAscii(text):
    #for ger, nonger in german_charakters.iteritems():
    #    text = re_sub(ger,nonger,text)
    return text

def getArticleAuthor(article):
    """
    getArticleAuthor(BeautifulSoup) -> (String,String)
    
    extracts the author from the article.

    param article:BeautifulSoup - the article site
    """
    try:
        author = article.find_all('p', attrs={'class':'author'})
        author = author[0].a.text
    except:
        author = 'NULL'
    return 'author',_makeAscii(author)

def getArticleContent(article):
    """
    getArticleContent(BeautifulSoup) -> (String,String)
    
    extracts the article Content.

    param article:BeautifulSoup - the article site
    """
    content = ""
    head = article.find_all('h2', attrs={'class':'article-title'})
    content += head[0].text + '\n\n'
    for s in article.find_all('p'):
	content += s.text
        if s.text.endswith(
                'Genehmigung der SPIEGELnet GmbH'):
            break
    return 'content',_makeAscii(content)

def getArticleDate(article):
    """
    getArticleDate(BeautifulSoup) -> (String,String)
    
    extracts the date when published.
    
    param article:BeautifulSoup - the article site
    """
    timeArt = article.find_all('time',
	    attrs={'itemprop':'datePublished'})
    published = timeArt[0].get('datetime')
    return 'published', published

def getArticleTimestamp(article):
    """
    getArticleTimestamp(BeautifulSoup) -> (String,int)
    
    extracts the timestamp when published.
    
    param article:BeautifulSoup - the article site
    """
    timeArt = article.find_all('time',
	    attrs={'itemprop':'datePublished'})
    published = timeArt[0].get('datetime')
    timeStr = strptime(published, "%Y-%m-%d %H:%M:%S") 
    timestamp =int(mktime(timeStr))
    return 'timestamp', timestamp

def getArticleTags(article):
    """
    getArticleTags(BeautifulSoup) -> (String,[String])
    
    extracts the article tags.
    
    param article:BeautifulSoup - the article site
    """
    tag = article.find_all('div',
		attrs={'class':'asset-box article-topic-box '})
    tags = []
    if tag != []:
        for t in tag[0].find_all('a'):
	    tags.append(t.text.lower())
    tag = article.find_all('div',attrs={'id':'breadcrumb'})
    if tag != []:
        tag = tag[0].find_all('a')
        for t in tag:
            if t.text.lower() not in tags:
                tags.append(t.text.lower())
    newtags = []
    for t in tags:
        newtags.append(_makeAscii(t))
    return 'tags', newtags

def getArticleCommmentExistence(article):
    """
    getCommentExistence(BeautifulSoup) -> (String,int)

    checks if the article has a comment section.
    
    param article:BeautifulSoup - the article site
    """
    if article.find_all('div'
		, attrs={'class':
                'clearfix article-comments-box module-box'}) == []:
	comment = 0
    else:
	comment = 1
    return 'comment', comment
