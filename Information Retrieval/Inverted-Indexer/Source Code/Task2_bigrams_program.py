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
from collections import OrderedDict
import operator
from prettytable import PrettyTable

indir = 'C:/Users/Tanvi/Desktop/HW3_Folder_to_upload/Corpus'

doc_id_dict = OrderedDict()
d = {}
n = 1
count = 0

#create a dictionary for filename as numbers
for filename in os.listdir(indir):
	f1 = indir + filename
	doc_id_dict[f1] = n
	n = n + 1

# read each file from the corpus and tokenize it 
# add the document to the inverted index of the term in tokens
# if term is already present increment its frequency in the document
# by 1
for t in doc_id_dict:
	docid = doc_id_dict[t]
	file = open(t, 'r')
	for line in file:
		t = line.split()
		#get bigrams
		tokens = zip(t,t[1:])
	

	for token in tokens:
		if token not in d:
			d[token] = {}
			d[token][docid] = 1
		elif docid in d[token].keys():
			d[token][docid] = d[token][docid] + 1
		else:
			d[token][docid] = 1	

#print d

tfindex = {}
for key in d:
	c = 0
	
	for doc in d[key]:
		
		c = c + d[key][doc]
		
	tfindex[key] = c
	

print "tf index:-------------"

#sort the index on term
sortedTF = sorted(tfindex.items(),key=operator.itemgetter(1), reverse = True)
#print sortedTF

bigram_tf = open('bigram_tf.txt', 'w')

for k in sortedTF:
	bigram_tf.write(str(k) + "\n")

d1 = OrderedDict()

for key in d:
	#print "new key---------"
	d1[str(key)] = [s for s in d[key]]

print "Dictionary----------------"
#sortedDict = sorted(d1.items())

#sort the inverted index on term and get term and documents and write into file
with open('bigram_doc_freq.txt','w+') as file:
	for key in sorted(d1):
		file.write(str(key) + "   :   " + str(d1[key]) + "    :    " + str(len(d1[key])) + "\n")
		