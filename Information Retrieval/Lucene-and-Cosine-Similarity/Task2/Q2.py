import pickle
from collections import OrderedDict
import math
import collections
from math import sqrt
import operator
from prettytable import PrettyTable

class cosine_similarity:
	query_dict = OrderedDict()
	idf = OrderedDict()
	normalized_tf = OrderedDict()
	dot_prod = OrderedDict()
	cos_sim = OrderedDict()

	# store the tf.idf for each query term in this dict
	tf_idf_query = OrderedDict()

	# store the tf.idf for each document in this dict
	tf_idf_doc_dict = OrderedDict()

	

	# open the file location where the table for each query is to be created
	def create_index_table_for_query(self, query_id):
		return open('C:/Users/Tanvi/Desktop/HW4_Tanvi_Ranadive/Tables/Table_Q2_Query' + str(query_id)+ '.txt', 'w+')
		



	# load the file containing all the docId with the 
	# total number of tokens in corresponding doc into a dictionary
	file = open("doc_tokens_dump.txt",'r')
	doc_tokens_dict = pickle.load(file)
	file.close()

	# load the file containing all the docId with all the 
	# terms in corresponding doc into a dictionary
	file = open("doc_terms_file.txt",'r')
	doc_terms_dict = pickle.load(file)
	file.close()

	# load the inverted index file into a dictionary
	file = open("inverted_index_dump.txt",'r')
	inverted_index_dict = pickle.load(file)
	#print "Inverted----"
	#print inverted_index_dict
	file.close()

	# load the file containing document name and corresponding docId
	# into a dictionary
	file = open("Dociddict.txt",'r')
	docid_dict = pickle.load(file)
	inv_docid_dict = {v: k for k, v in docid_dict.iteritems()}
	print "inverted-----"
	print docid_dict
	file.close()

	# load the file containing the queries into a dictionary
	file = open("queries.txt","r")
	for line in file:
		line = line.strip()
		k = line[0:1]
		query_dict[k] = line[2:]



	# main function to calculate the cosine similarity score for each query	
	def main_function_all_queries(self):
		for q in self.query_dict:
			self.cos_similarity_for_all_docs(self.query_dict[q], q)

	

	# calculate the cosine similarity for each document and rank them
	# write the top 100 ranked documents to a file
	def cos_similarity_for_all_docs(self, query, query_id):
		#get the idf for all docs
		self.get_idf_docs(query)

		# get the normalized term frequencies for each query term
		self.get_normalized_tf(query)

		# get the tf.idf for documents
		self.get_tf_idf_for_docs(query)

		# get the tf.idf for the query
		self.get_tf_idf_for_query(query)

		# get the cosine similarity for the query and each document
		for doc in self.docid_dict:
			docid = self.docid_dict[doc]
			self.cos_similarity(query, docid)

		# after iterating through all the documents, sort the documents based on 
		# their cosine similarity score	and write the top 100 documents to a file

		od = OrderedDict(sorted(self.cos_sim.items(), key = lambda(k,v):(v,k), reverse = True))	
		
		table = PrettyTable(['query_id','Q0','doc_id','rank','CosineSim_score','system_name'])
		index = self.create_index_table_for_query(query_id)
		#index = open('C:/Users/Tanvi/Desktop/HW4_Tanvi_Ranadive/Table_Query' + str(query_id)+ '.txt', 'w+')
		rank = 1
		for key,value in od.items():
			if rank <= 100:
				table.add_row([query_id,"Q0",str(key) + " (" + (str(self.inv_docid_dict[key]))[49:-4] + ") ",rank,value,"Tanvi"])
				rank = rank + 1
			else:
				break	
		print table
		# write to file
		index.write(table.get_string())	



	# get idf for the query for each doc and store in dictionary	
	def get_idf_docs(self, query):
		terms = query.split(" ")
		#print terms
		for t in terms:
			sum = 1 + math.log(len(self.docid_dict)/len(self.inverted_index_dict[t]))
			self.idf[t] = sum



	# get the normalized tf for each term and store in a dictionary		
	def get_normalized_tf(self, query):
		terms = query.split(" ")
		for t in terms:
			self.normalized_tf[t] = {}				
			for docid in self.inverted_index_dict[t].keys():
				temp = self.inverted_index_dict[t][docid]
				normalized = float(temp)/float(self.doc_tokens_dict[docid])
				self.normalized_tf[t][docid] = normalized



	# get the tf.idf for the query terms for each doc and store in dictionary			
	def get_tf_idf_for_docs(self, query):
		for t in query.split(" "):
			for doc in self.inverted_index_dict[t]:
				if doc not in self.tf_idf_doc_dict:
					self.tf_idf_doc_dict[doc] = {}
					self.tf_idf_doc_dict[doc][t] = self.normalized_tf[t][doc] * self.idf[t]
				else:
					self.tf_idf_doc_dict[doc][t] = self.normalized_tf[t][doc] * self.idf[t]
					
							

	# get tf.idf for the query				
	def get_tf_idf_for_query(self, query):
		terms = query.split(" ")
		counter = collections.Counter(terms)
		total_terms_query = len(terms)
		for t in terms:
			self.tf_idf_query[t] = (float(counter[t])/float(total_terms_query)) * self.idf[t]	



	# calculate cosine similarity for a query and a document
	def cos_similarity(self, query, doc):
		doc_magnitude = 0
		terms = query.split(" ")

		# if document does not contain the query term, set its value to 0
		# else calculate its cosine similarity score
		if doc not in self.tf_idf_doc_dict:
			self.cos_sim[doc] = 0
		else:

			# iterate through the document and if the document does not contain the
			# query term, move to the next term and calculate document magnitude
			doc_magnitude = self.get_doc_magnitude(doc)
			
			# if denominator is 0, put the cosine similarity score as 0,
			# else store the score for the document in dictionary		
			if 	float(self.query_magnitude(query) * doc_magnitude) == 0:
				c = 0
			else:
				c = float(self.dot_product(query, doc))/ float(self.query_magnitude(query) * doc_magnitude)
			self.cos_sim[doc] = c		


	# get the document magnitude of a document
	def get_doc_magnitude(self, doc):
		totalmag = 0
		#print doc
		print " doc -----" + str(doc)
		for term,frequency in self.doc_terms_dict[doc].items():
			
			#print "total numbe rof tokens in doc-----"
			#print self.doc_tokens_dict[doc]
			b = float(frequency) / float(self.doc_tokens_dict[doc])
			#print "b----" + str(b)
			p = 1 + math.log(len(self.docid_dict) / len(self.inverted_index_dict[term]))
			docValue = b * p
			totalmag = totalmag + docValue ** 2
		return sqrt(totalmag)
				

	# calculate the query magnitude for given query
	def query_magnitude(self, query):
		qmag = 0
		for t in query.split(" "):
			qmag = qmag + (self.tf_idf_query[t])**2
		return sqrt(qmag)	


	# calculate the dot product	of tf.idf of query and document and return it
	def dot_product(self, query, doc):
		terms = query.split(" ")
		dp = 0
		for t in terms:
			if doc in self.inverted_index_dict[t]:
				self.tf_idf_query[t]
				self.tf_idf_doc_dict[doc][t]
				dp = dp + (self.tf_idf_query[t] * self.tf_idf_doc_dict[doc][t])
				self.dot_prod[doc] = dp
			else:
				self.dot_prod[doc] = dp
		return dp


# create an object of the class and call the main function
obj = cosine_similarity()
obj.main_function_all_queries()