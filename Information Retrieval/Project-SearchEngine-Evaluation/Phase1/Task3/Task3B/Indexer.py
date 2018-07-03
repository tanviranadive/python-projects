__author__ = 'shraddha shah'

import os
from collections import OrderedDict
from collections import Counter
import json
import pickle
from prettytable import PrettyTable
import sys
import operator
reload(sys)
sys.setdefaultencoding('utf-8')

class IndexCreator:

	# rootdir = '/Users/Shraddha/Desktop/HW-3-Shraddha/Task1/ParsedCorpus'
	termFrequency = OrderedDict()
	documentFrequency = OrderedDict()
	invertedIndex = {}
	docID = OrderedDict()
	nGrams = {}
	nGrams[1] = "unigram"
	nGrams[2] = "bigram"
	nGrams[3] = "trigram"
	tokenCount = OrderedDict()
	tokensForDoc = OrderedDict()
	

	def docToID(self,rootdir):
		""" input  : Path of directory of the corpus to be indexed
		    output : dictionary of mapping of doc name to doc id
		"""
		i = 1
		for file in os.listdir(rootdir):
			if (file != '.DS_Store'):
				self.docID[file.strip(".txt")] = i
				i = i + 1
		with open("doctoID.p", 'wb') as file:
			pickle.dump(self.docID, file)
		

	def getTokensInADoc(self):

		# dumping tokens and it's frequency for each document

		with open("tokenCount.p", 'wb') as file:
			pickle.dump(self.tokenCount, file)
		
		return self.tokenCount

	def getTokens(self):
			
		with open("tokensInDoc.p", 'wb') as file:
			pickle.dump(self.tokensForDoc, file)
		
		return self.tokensForDoc


	def getIndex(self, rootdir, n):
		""" input  : Path of directory of the corpus to be indexed
					 no of grams
					 
		    output : inverted index for the corpus
		"""
		# print stopList
		for file in os.listdir(rootdir):
			if (file != '.DS_Store'):
				doc = open(rootdir + file)
				dID = self.docID[file.strip(".txt")]
				print(dID)
				t = (doc.read().split())
				tokens = []
				if (n == 1):
					tokens = t
				if (n == 2):
					tokens = zip(t,t[1:])
				if (n == 3):
					tokens = zip(t, t[1:], t[2:])

				docTokens = Counter(tokens)
				self.tokensForDoc[dID] = docTokens
				

				self.tokenCount[dID] = sum(docTokens.values())


				for token, count in docTokens.items():
					if not token.isdigit():
						if token not in self.invertedIndex:
							self.invertedIndex[token] = {}
						self.invertedIndex[token][dID] = count
				doc.close()

		return self.invertedIndex

	def dumpIndex(self, invertedIndex, n):
		""" input  : inverted index of the corpus
		             n for the n-gram
		             
		    output : dumps inverted index to a .txt file
		"""
		

		with open("invertedindex_" + str(self.nGrams[n]) + ".p", 'wb') as f:
			# json.dump(invertedIndex, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ':'))
			pickle.dump(invertedIndex, f)

	def storeDocStatistics(self, invertedIndex, n):
		""" input  : inverted index of the corpus
		    output : dumps doc statistics like term frequency and doc frequency to .txt files
		"""

		self.dumpTermFrequency(self.invertedIndex, n)
		self.dumpDocumentFrequency(self.invertedIndex, n)

	def dumpTermFrequency(self, invertedIndex, n):
		""" input  : inverted index of the corpus
		    output : dumps term frequency table to .txt files
		"""
		
		for term in invertedIndex:
			list = invertedIndex[term]
			frequency = 0
			for id in list:
				frequency = frequency + list[id]
			self.termFrequency[term] = frequency

		file = open("termfrequency_" + str(self.nGrams[n]) + ".txt", 'w')
		table = PrettyTable(['Term', 'Frequency'],sortby = "Frequency", reversesort = True)
		table.border = True
		table.align = "c"
		for key, val in self.termFrequency.items():
		   table.add_row([key, val])
		file.write(table.get_string())

	def dumpDocumentFrequency(self, invertedIndex, n):
		""" input  : inverted index of the corpus
		    output : dumps document frequency table to .txt files
		"""

		
		for term in invertedIndex:
			self.documentFrequency[term] = [s for s in invertedIndex[term]]
		
		file = open("documentfrequency_" + str(self.nGrams[n]) + ".txt", 'w')

		for key in sorted(self.documentFrequency):
		   file.write(str(key) + " : " + str(self.documentFrequency[key]) + ",   " + str(len(self.documentFrequency[key])) + "\n")

    


		


