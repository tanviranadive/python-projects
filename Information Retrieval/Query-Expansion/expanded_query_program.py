#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#from __future__ import unicode_literals
import pickle
import io
import os
import sys
import re
import collections
from math import log
import operator
import nltk
from nltk import word_tokenize
import math
reload(sys)
sys.setdefaultencoding("UTF-8")
from collections import OrderedDict

class QueryExpansion:
	

	file2='BM25_top_5_docs.txt'
	fr1=open(file2,'r')
	top_docs = pickle.load(fr1)
	print "top docs---"
	print top_docs
	regex = re.compile("^[0-9]+$")


	file3='tf_idf_dict.txt'
	fr2=open(file3,'r')
	tf_idf_dict = pickle.load(fr2)


	def get_tf_idf_sorted(self):
		sorted_tf_idf = {}
		for doc in self.tf_idf_dict:
			sorted_tf_idf[doc]={}
			entry=self.tf_idf_dict[doc]
			entry_new={}
			entry_new= sorted(entry.iteritems(), key=lambda (k,v): (v,k),reverse=True)
			sorted_tf_idf[doc]=entry_new
		return sorted_tf_idf


	def get_expanded_query(self,num,sorted_dict,fw1):
			for doc in self.top_docs[num]:
				count=0
				entry={}
				entry=sorted_dict[doc]
				for key, value in entry:
					if count<2:
						if not re.match(self.regex,key):
							count=count+1
							fw1.write(str(key +" "))
			fw1.write("\n")				


		
file1='queries.txt'
fr=open(file1,'r')
file2='Expanded_queries.txt'
fw1=open(file2,'w')	
qexp = QueryExpansion()
num=0
sorted_dict=qexp.get_tf_idf_sorted()
for line in fr:
	num=num+1
	query_text=line.strip('\n')
	query_text = query_text.lower()
	fw1.write(str(query_text) + " ")
	qexp.get_expanded_query(num,sorted_dict,fw1)
