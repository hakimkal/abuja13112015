import bs4
from bs4 import BeautifulSoup
import requests
import csv
import time
from xhtml2pdf import pisa   
url = 'http://radar.techcabal.com'
url1 = "http://radar.techcabal.com/categories"
url2 = "http://radar.techcabal.com/latest"

class Objectify:
	def __init__(self,**args):
		self.__dict__.update(args)
		
def openRadar():
	try:
		r = requests.get(url2)
		bsText = BeautifulSoup(r.text, 'html.parser')
		#htmldoc = "radarText.txt"
		#bsText = BeautifulSoup(open(htmldoc), 'html.parser')
	except:
		htmldoc = "radarText.txt"
		bsText = BeautifulSoup(open(htmldoc), 'html.parser')
		

	
	
	#print bsText
	allDivs = bsText.find_all('div')
	#print allDivs
	#print allDivs[0:7]
	postCounts = []
	posts = []
	for div in allDivs[:7]:
		meta = div.find_all('meta')[0]
		#print meta
		link = meta.get('content')
		#print link
		
		postComments = meta.find_all('span')[-1]
		#print postComments
		postcount =  postComments.contents[1].contents[0]
		comments_url = postComments.contents[1].get('href')
		postCounts.append(int( postcount))
		posts.append(dict({'url':link,'count':int(postcount), 'comments_url': comments_url}))
	#print posts
	item  = max(postCounts)	
	getPost(posts,item)
	
def getPost(posts, count):
	for p in posts:
		print p
		post = Objectify(**p)
		if post.count  == count:
			getPostAndComments(post)
		break


def getPostAndComments(post):
	try:
		 
		r = requests.get(post.url)
		
		p = BeautifulSoup(r.text, 'html.parser')
		
		pdf = makePDF(r.text,post.url)
		
		print "checkFile"
	except Exception,e:
		raise e
		print "No internet connection detected"
		exit
	
 
from selenium import webdriver
 

def get_browser_html(url):
	
	browser = webdriver.Chrome('/home/abdulhakim/Downloads/chromedriver')
	browser.get(url)
	
	
	html_source = browser.page_source
	return html_source,browser
	
def makePDF(post,url=None):
	 
	#print post
	outputFilename =  str(time.time()).replace(".","") + ".pdf"
	import pdfcrowd
	client = pdfcrowd.Client("hakeemhal", "4fde3d60fe495aaf8ca7a420330991ce")
	print url
	html,browser = get_browser_html(url)
	 
	
	output_file = open(outputFilename,'wb')
	print "Converting to pdf..."
	client.enableJavaScript(False)
	pdf = client.convertHtml(html,output_file)
	output_file.close()
	print "File ", outputFilename, "created"
	browser.close()


openRadar()