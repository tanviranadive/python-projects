import pickle
import math
import operator
from collections import OrderedDict
import sys
import collections
from math import log
from decimal import Decimal
from prettytable import PrettyTable

class BM25:

	#specify the location where the output table for each query is to be created
	outfile = 'C:/Users/Tanvi/Desktop/HW4_Tanvi_Ranadive/bm25/BM25_Query'


	# load the inverted index file into a dictionary
	file = open("inverted_index_dump.txt",'r')
	inverted_index_dict = pickle.load(file)
	file.close()

	# load the file containing all the docId with the 
	# total number of tokens in corresponding doc into a dictionary
	file = open("doc_tokens_dump.txt",'r')
	doc_tokens_dict = pickle.load(file)
	file.close()

	# load the file containing all the docId with all the terms in that doc
	# and their frequency in corresponding doc into a dictionary
	file = open("doc_terms_file.txt",'r')
	doc_terms_dict = pickle.load(file)
	file.close()

	# load the file containing all the docId into a dictionary
	file = open("Dociddict.txt",'r')
	doc_id_dict = pickle.load(file)
	inv_docid_dict = {v: k for k, v in doc_id_dict.iteritems()}
	file.close()

	# empirical constants for bm25
	k1= 1.2
	k2=100
	b=0.75
	avdl = 0
	R = len(doc_tokens_dict)


	def main_function (self):
		qcount = 0
		self.calcAvgDocLength()
		with open('queries.txt', 'rb') as queryfile:
			for line in queryfile:
				line = line.strip()
				qcount = qcount + 1
				bm25score = {}

				# calculate bm25 scores for each query
				self.calculateBM25score(line, bm25score)

				# sort teh documents based on bm25 scores
				sortedBM25 = OrderedDict(sorted(bm25score.items(), key = lambda(k,v):(v,k), reverse = True))		
				table = PrettyTable(['query_id','doc_id','rank','bm25_score'])
				index = open(self.outfile + str(qcount)+ '.txt', 'w+')
				rank = 1
				for key,value in sortedBM25.items():
					table.add_row([qcount,str(key) + " (" + (str(self.inv_docid_dict[key]))[49:-4] + ") ",rank,value])
					rank = rank + 1	
				print table
		# write to file
				index.write(table.get_string())	


	# calculate the frequency of each term in query			
	def calcqf(self, query):
		terms = query.split(" ")
		qf = collections.Counter(terms)
		#print "qf -------" + str(query)
		#print qf
		return qf		
		


	# calculate the average document length
	def calcAvgDocLength (self):
		sumlength = 0
		for doc in self.doc_tokens_dict:
			sumlength = sumlength + self.doc_tokens_dict[doc]
		self.avdl = sumlength/len(self.doc_tokens_dict)
		print "avg doc length-----" + str(self.avdl)


					
	# calculate the bm25 score for each document and store it in a dictionary
	def calculateBM25score(self, query, bm25score):
		print "query-----" + str(query)
		qf = self.calcqf(query)
		terms = query.split(" ")
		for key in self.doc_terms_dict:			

			dl = self.doc_tokens_dict[key]
			K = float(self.k1* ((1-self.b) + float((self.b*dl)/float(self.avdl))))
			#print "doc :----" + str(key)

			# since no relevance information is available, ri and R will be 0 in this case
			for t in terms:

				if t in self.doc_terms_dict[key]:

					b = float((len(self.doc_tokens_dict) - len(self.inverted_index_dict[t]) + 0.5)/ (len(self.inverted_index_dict[t]) + 0.5))

					value = self.doc_terms_dict[key][t]

				else:

					b = float((len(self.doc_tokens_dict) - len(self.inverted_index_dict[t]) + 0.5)/ (len(self.inverted_index_dict[t]) + 0.5))
					
					# term not present in the document
					value = 0

				#print "value ----" + str(t) + str(key) + "   " + str(value)	
				m = float(((((self.k1 + 1) * value) + 1)/ (K + value + 1)) * (((self.k2 + 1) * qf[t])/ (self.k2 + qf[t])))

				#m = float((((self.k1 + 1) * value)/ (K + value)) * ((self.k2 + 1) * qf[t])/ (self.k2 + qf[t])) + 0.5

				score = math.log(b*m)
				#print score	

				# Add the bm25 score for the document for each query term
				if key in bm25score:
					bm25score[key] = bm25score[key] + score
				else:
					bm25score[key] = score			



obj = BM25()
obj.main_function()				