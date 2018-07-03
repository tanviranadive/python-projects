__author__ = 'shraddha shah'

import pickle
from collections import OrderedDict
import math
import operator
from prettytable import PrettyTable
import nltk
from nltk import word_tokenize

class Ranker:
    # dictionary of doc id to list of tokens in that doc
	tokensInDoc = pickle.load(open("tokensInDoc.p","rb"))

	# dictionary of doc id to no of tokens in that doc
	tokenCount = pickle.load(open("tokenCount.p","rb"))

	# index for the corpus
	index = pickle.load(open("invertedindex_unigram.p","rb"))


	def getRankedDocuments(self, queries):
		"""input: path of the file in which queries are there
		   ouput: writes the top 100 scored documents in "VSMRanking.txt"
		"""
		queryId = 0
		for query in queries:
			queryId = queryId + 1
			queryTerms = query.split()
			
			queryInvertedList = OrderedDict()
			
			# dictionary of query terms and it's TF*IDF score
			queryTFIDF = OrderedDict()
			

			for term in queryTerms:
				if term in self.index.keys():

					queryInvertedList[term] = self.index[term]
					queryTFIDF[term] = (float(queryTerms.count(term))/len(queryTerms)) * (1.0 + math.log(float(len(self.tokenCount))/len(queryInvertedList[term])))
		
			# dictionary of query terms in document and it's TF*IDF score
			docTFIDF = OrderedDict()

			for term in queryInvertedList:
				entry = queryInvertedList[term]
				for docID in entry:
					if docID not in docTFIDF:
						docTFIDF[docID] = {}
					docTFIDF[docID][term] = float(entry[docID])/self.tokenCount[docID] * (1.0 + math.log(float(len(self.tokenCount))/len(queryInvertedList[term])))
		
			# dictionary of doc id and it's cosine score
			docScore = OrderedDict()

			for docID in docTFIDF:
				termList = docTFIDF[docID]
				docScore[docID] = 0
				for term in termList:
					docScore[docID] = docScore[docID] + queryTFIDF[term]*termList[term]
				docScore[docID] = docScore[docID]/(self.getMagnitude(queryTFIDF) * self.getMagnitude(self.getTotalDoc(docID)))

			sortedScore = OrderedDict(sorted(docScore.items(), key=operator.itemgetter(1), reverse=True))

			doctoID = pickle.load(open("doctoID.p","rb"))

			doctoID = {v: k for k, v in doctoID.iteritems()}

			rank = 0
			file = open("VSMRanking.txt" , 'a')
			outputFile = open("VSMStats.txt", 'a')
			file.write("Query: " + query)
			table = PrettyTable(['QueryID', 'Literal', 'DocID', 'Rank', 'Score', 'SystemName'])
			table.border = True
			table.align = "c"
			for key, value in sortedScore.items():
				rank = rank + 1
				if(rank <= 100):
					table.add_row([queryId, " Q0 ", str(key) + "(" + doctoID[key] + ")" ,rank , value, "shraddha"])
					outputFile.write(str(queryId) + " " + str(rank) + " " + str(key) + " " + str(value))
					outputFile.write('\n')
				else:
					break
			file.write("\n")
			file.write(str(table))
			file.write("\n")



	def getMagnitude(self, dict):
		""" input: a dictionary
		    output: magnitude of all the scores for all the key in the dictionary
		"""
		sum = 0
		for term in dict:
			sum = sum + dict[term]*dict[term]

		return math.sqrt(sum)

	def getTotalDoc(self, docId):
		""" input: doc id
		    output: dictionary of tokens and it's TF*IDF score for the given docID
		"""
 
		# dictionary of tokens and it's TF*IDF score for the given docID
		docTotalTFIDF = OrderedDict()
		dict = self.tokensInDoc[docId]
		for token, count in dict.items():
			docTotalTFIDF[token] = float(count)/self.tokenCount[docId] * (1.0 + math.log(float(len(self.tokenCount))/len(self.index[token])))

		return docTotalTFIDF





		    

			

