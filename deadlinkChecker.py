# -- coding: utf-8 --
#!/usr/bin/python


"""
Python2.7 is default environment
Created on November 11, 2015

@author: hakeemhal

pip install requests
pip install beautifulSoup4
"""
 
import  json, os, sys
import requests
import bs4
from bs4 import BeautifulSoup

print "Beautiful Soup Version: " + bs4.__version__ 
print "Json Version: " + json.__version__
print "Requests Version: " + requests.__version__


#convert dictionary to object
class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)
def header(allLinks=[]):
	 print "*" * 12
	 
	 print "We found %s UrLs on the page" %(len(allLinks) - 1)
	 
	 
def result(string):
	print string

def checkLinks(links = []):
	#print links
	header(links)
	
	for link in links:
		link = Struct(**link)
		try:
			result(isValidUrl(link.url,link.linkText))
		except:
			print 'ErrorLink :\t\t\t %s' %(link)

def isValidUrl(url,linkText):
	try:
		if url.startswith('http://') or url.startswith("https://"):
			r = requests.get(url)
			if r.status_code == 200:
				return "Url: %s \t\t\t| \t\t\t ActiveLink!"%(url)
			elif r.status_code == 404:
				return "URL: %s \t\t\t| Text: %s \t\t\t| DeadLink!" %(url,linkText)
			else:
				return "URL: %s \t\t\t| \t\t\tDeadLink!" %(url)
		else:
			return "URL: %s\t\t\t| Incomplete Url"%(url)
			
	except RuntimeError:
		pass
	
	
def getPage(url=None):
	if url is None:
		url  = raw_input("Enter Url (Ex: http://*)")
	
	u = Struct(**goToUrl(url))
	#u.code
	bsText = BeautifulSoup(u.text, 'html.parser')	
	
	filterLinks = bsText.find_all('a')
	allLinks = []
	allLinks.append(dict({'linkText': 'Main Link', 'url':u.url}))
	
	for l in filterLinks:
		allLinks.append(dict({'linkText': l.contents[0] , 'url':l.get('href')}))
	checkLinks((allLinks))
		
		

def goToUrl(url):
	r = None
	try:
		r = requests.get(url)
		return dict({'code': r.status_code,'headers': r.headers['content-type'],'text': r.text,'url': url})
	except:
		print "Could not establish connection to the specified URL : %s" %(url)
		exit()
		
if __name__ == '__main__':
	if len(sys.argv) > 1:
		getPage(sys.argv[1])
	else:
		getPage()




