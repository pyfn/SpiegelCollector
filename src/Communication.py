"""
Namespace for Communication functions

Downloading relevant articles from Spiegel.de
"""


from bs4 import BeautifulSoup as bs
from urllib2 import urlopen
from utils import BuildUtil

#standard Spiegel domain
BASE_LINK = 'http://www.spiegel.de/'


def getArticleList(date):
	"""
	getArticleList(String) -> [String]

	returns a List with all published articles at the given date

	param date:String - Specified date to scrape all
	  - articles(dd-mm-YYYY)
	"""
	articleLinks = []
        dates = date.split('-')
	day = bs(urlopen(BASE_LINK + 
		'nachrichtenarchiv/artikel-{}.{}.{}.html'.format(
		*dates)).read())
	#looping over all conatainers for links
	for i in bs(str(day.find_all('div', 
		attrs={'class':'column-wide'}))).find_all('a'):
		articleLinks.append(str(i.get('href')))
	return articleLinks
    
def getArticle(link):
	"""
	getArticle(String) -> Dictionary

	returns a Dictionary with useful data (date, text, existence 
	  - of the comment section)

	param link:String - The specific link to scrape
	"""
	if not link.startswith('http://www.') or link.startswith('https://www.'):
		link = BASE_LINK + link.strip('/')
	article = bs(urlopen(link))
        articleDict = {}
	#putting everyting in a Dictionary with every attribute
        #BuildUtil extracts.
        for funcName,func in BuildUtil.__dict__.iteritems():
                if callable(func):
                        if funcName.startswith('getArticle'):
                                name, value = func(article)
                                articleDict[name] = value
        articleDict['link'] = link
        articleDict['site'] = link.split('www.')[1].split('.')[0]
        articleDict['articleid'] = 'NULL'
	return articleDict
