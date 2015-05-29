from src import Communication
from src import DataManager
from time import sleep

def main():
	articles = []
	count = 0
	for i in range(5):
		try:
			arts = Communication.getArticleList('29-05-2015')
			break
		except Exception as e:			
			print e
			if i == 4:
				print 'Check your connection!'			
			sleep(3)
			
	
	for article in arts:
		if DataManager.artExists(article) and ('panorama' not in article.lower()):	
			try:				
				print '[+] Downloading: ' + article
				DataManager.storeArticle(
					article=Communication.getArticle(article))
				print '[+] ' + articles[-1]['link']
				count += 1
			except Exception as e:
				print '[!] Error with article: {}'.format(article)
				print e
				continue
	print 'finished downloading {} articles'.format(count)

if __name__ == '__main__':
	main()
