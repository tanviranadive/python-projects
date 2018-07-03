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
import json
from prettytable import PrettyTable
import pickle
import collections

indir = 'C:/Users/Tanvi/Desktop/HW4_Tanvi_Ranadive/Corpus/'

doc_id_dict = OrderedDict()
d = {}
doc_tokens_dict = {}
n = 1
count = 0
#dictionary for number of tokens in each document
numtokens = {}

#create a dictionary for filename as numbers
for filename in os.listdir(indir):
	f1 = indir + filename
	#print f1
	doc_id_dict[f1] = n
	n = n + 1


with open("C:/Users/Tanvi/Desktop/HW4_Tanvi_Ranadive/Task2/Indexer/doc_id_dict.txt", 'w') as docidtable:
	for doc in doc_id_dict:
		docidtable.write(str(doc) + "  :  " + str(doc_id_dict[doc]) + "\n")

filehandler = open("Dociddict.txt","w+")
pickle.dump(doc_id_dict,filehandler)
filehandler.close()

doc_terms_dict = OrderedDict()

# read each file from the corpus and tokenize it 
# add the document to the inverted index of the term in tokens
# if term is already present increment its frequency in the document
# by 1
#f1 = open('doc_tokens_file.txt','w+')
#f2 = open('doc_terms_file.txt','w+')
for t in doc_id_dict:
	docid = doc_id_dict[t]
	file = open(t, 'r')
	f = file.read().decode('utf-8')
	tokens = nltk.word_tokenize(f)
	#tm = tokens.split(" ")
	counter = collections.Counter(tokens)
	doc_terms_dict[docid] = counter
	#print "number of tokens in doc" + str(t)
	#print len(tokens)


	doc_tokens_dict[docid] = len(tokens)
	#with open('doc_tokens_file.txt','a') as f1:
		#f1.write(str(docid) + "     " + str(len(tokens)) + "\n")
		


	#add the total number of tokens of document t into a dictionary numtokens
	numtokens[t] = len(tokens)
	for token in tokens:
		if token not in d:
			d[token] = {}
			d[token][docid] = 1
		elif docid in d[token]:
			d[token][docid] = d[token][docid] + 1
		else:
			d[token][docid] = 1

#print d
filehandler = open("inverted_index_dump.txt","wb")
pickle.dump(d,filehandler)
filehandler.close()

filehandler = open("doc_tokens_dump.txt","w+")
pickle.dump(doc_tokens_dict,filehandler)
filehandler.close()

tfindex = {}
for key in d:
	c = 0
	for doc in d[key]:
		c = c + d[key][doc]
	tfindex[key] = c

print "tf index:-------------"
#number of unique tokens
#print len(tfindex.keys())

filehandler = open("tfindex_dump.txt","wb")
pickle.dump(tfindex,filehandler)
filehandler.close()

#print doc_terms_dict
filehandler = open("doc_terms_file.txt","w+")
pickle.dump(doc_terms_dict,filehandler)
filehandler.close()

index = open('C:/Users/Tanvi/Desktop/HW4_Tanvi_Ranadive/Task2/Indexer/unigram_index1.txt', 'w')

#create prettytable for term frequency table
table = PrettyTable(['Term','TermFrequency'])

for key,value in tfindex.items():
	table.add_row([key,value])

index.write(table.get_string(sortby="TermFrequency",  reversesort=True))

print "sorted dict ----------"
#print sortedDict

d1 = OrderedDict()
#sort the inverted index on term and get term and documents into d1
for key in d:
	print "new key---------"
	d1[str(key)] = [s for s in d[key]]
			

print "Dictionary----------------"
#print d1

#print document frequncy into file
with open('C:/Users/Tanvi/Desktop/HW4_Tanvi_Ranadive/Task2/Indexer/unigram_doc_freq.txt','w+') as file:
	for key in sorted(d1):
		file.write(str(key) + "   :   " + str(d1[key]) + "    :    " + str(len(d1[key])) + "\n")

