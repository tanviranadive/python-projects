from bs4 import BeautifulSoup

import requests
import re
import sys
import codecs
import urllib2
import string
reload(sys)
import nltk
from nltk import word_tokenize
from urlparse import urljoin
sys.setdefaultencoding('utf-8')
import time
import os

indir = 'C:/Users/Tanvi/Desktop/HW3_Folder_to_upload/HTML Pages'


regex = re.compile('[%s]' % re.escape(string.punctuation))
remove_char = (':',";"," - ",". ","\'","-\ ")
filedict = {}	

for filename in os.listdir(indir):
	html = open(indir + filename, 'r')
	soup = BeautifulSoup(html, 'html.parser')
	page = soup.find("div", id = 'mw-content-text')
	print filename

	for div in page.find_all("table"):
		div.extract()

	for div in page.find_all("img"):
		div.extract()

	for div in page.find_all("div", {'class':'script'}):
		div.extract()

	for div in page.find_all("div", {'class':'style'}):
		div.extract()

	for div in page.find_all("div", {'class':'noprint'}):
		div.extract()

	for div in page.find_all("div", {'class':'mw-editsection'}):
		div.extract()

	for div in page.find_all("div", {'class':'references'}):
		div.extract()

	for div in page.find_all("div", {'class':'reflist'}):
		div.extract()

	for div in page.find_all("span", {'id':'References'}):
		div.extract()

	for div in page.find_all("span", {'class':'mw-editsection'}):
		div.extract()

	for div in page.find_all("sup", {'class':'reference'}):
		div.extract()

	for div in page.find_all("div", {'class':'toc'}):
		div.extract()

	for div in page.find_all("div", {'class':'thumbcaption'}):
		div.extract()

	for div in page.find_all("div", {'class':'printfooter'}):
		div.extract()

	for div in page.find_all("img"):
		div.extract()


				

	#url = url.strip()
	#n = url[29:]
	n = filename
	n = n.replace(".txt","")
	c = 1
	#for files in filedict:
	if n not in filedict:
		filedict[n] = c
	else:	
		n = str(n) + str(c)
		filedict[n] = c

	n = regex.sub("",n)
	name = n + ".txt"

	file=open(name,'w')
	result = page.text.lower()
	remove_char = '!"#$%&' + "()*+/:;<=>?@[\]^_`{|}~"
	result = "".join(ch for ch in result if ch not in remove_char)
		#print result
	tokens = word_tokenize(result)
	for token in tokens:
			#t = token + " "
		token = re.sub(r'(?<!\d)\.|\.(?!\d)',"",token)
		token = re.sub(r'(?<!\d)\,|\,(?!\d)',"",token)
		token = re.sub(r'(?<!\d)\%|\$(?!\d)',"",token)
		token = re.sub(r'(?<!\d)\\|\\(?!\d)',"",token)
		token = re.sub(r'(?<![a-zA-Z0-9])\-|\-(?![a-zA-Z0-9])',"",token)
		file.write(str(token) + " ")
			#print str(token)
	print "all tokens-------"
	#print tokens		
		#file=open(name,'a')
		
		#for line in result:
			#line = line.lower()
			#print line
			#print "sothing else"
			#line.replace(remove_char," ")
			#file.write(line)
	file.close()

		#print page.text