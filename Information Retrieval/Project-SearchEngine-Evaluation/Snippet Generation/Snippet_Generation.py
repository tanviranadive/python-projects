#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#from __future__ import unicode_literals
import pickle
import io
import os
import sys
import collections
from math import log
import operator
import nltk	
from nltk import word_tokenize
import math
reload(sys)
import pickle
import string
sys.setdefaultencoding("UTF-8")
from collections import OrderedDict

#file = open('CACM-1410.html','rb')

output_file= open("Document_snippets.txt","w")

f= open("tf_idf_dict.txt","r")
tf_idf_dict = pickle.load(f)

f1= open("BM25_top_5_docs.txt","r")
top_docs_dict = pickle.load(f1)
#print top_docs_dict

f2= open("doctoID.p","r")
doc_id_dict = pickle.load(f2)

f3= open("queryFile.txt","r")
query_id_dict = pickle.load(f3)

inv_doc_id_dict ={v: k for k, v in doc_id_dict.iteritems()}
print inv_doc_id_dict

stopWords = []
stopListFile = open("common_words.txt", 'r')

for word in stopListFile:
	stopWords.append(word.strip())


remove_char = '!"#&,.' + "()*+':;<=>?@[]^_`{|}~"



def snippet_generation(query, file, d):
	q_tokens = query.split()
	#print q_tokens
	score = {}
	n = 0
	tokens= []
	for line in file:
	    tokens.extend(line.split())
	#print tokens

	i = 0
	score = {}

	while (i+20)!= len(tokens):
		window = tokens[i: i+20]
		#print str(i)
		#print window
		i = i + 1
		score[i] = 0
		for term in window:
			if not term.isdigit():
				score[i] = score[i] + tf_idf_dict[d][term]
				if (term in q_tokens) and (term not in stopWords):
				#print "yessss" + str(term)
					if i in score:
						score[i] = score[i] + 10
			else:
				score[i] = 0


	sortedp = sorted(score.iteritems(), key=lambda (k,v): (v,k),reverse=True)
	#print sortedp
	snippet= []
	for k in range(1):
		start= sortedp[k][0]
		snippet = tokens[start:start+20]
		#print snippet

	str1 = ""

	for ele in snippet:
		if (ele in q_tokens) and (ele not in stopWords):
			str1 = str1 + str("<b>" + ele + "</b> ")
		else:
			str1 = str1 +str(ele+ " ")	
	print "\n Document:- " + str(d) + " Snippet - "		
	print "..." + str1	+ "..."
	output_file.write("\n")
	output_file.write("\nDocument:- " + str(d) + " Snippet - \n")
	output_file.write("..." + str1	+ "...")


with open("Document_snippets.txt","a"):
	for qid in query_id_dict:
		query = query_id_dict[qid]
		output_file.write("\n")
		output_file.write("Query :- " + query)
		#query = "What articles exist which deal with TSS (Time Sharing System), an operating system for IBM computers?"
		query = "".join(ch for ch in query if ch not in remove_char)
		query = query.lower()
		for d in top_docs_dict[qid]:
			#docname = "/Users/Shraddha/Desktop/IR-Project/cleaned_cacm/" + inv_doc_id_dict[d]
			docname = "C:/Users/Tanvi/Downloads/IR-Project/cleaned_cacm/" + inv_doc_id_dict[d]
			file = open(docname,"r")
			snippet_generation(query,file,d)
		output_file.write("\n\n")	

