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
sys.setdefaultencoding("UTF-8")
from collections import OrderedDict


class BM25:
	rel_file = open("cacm_rel.txt","rb")
	rel_dict = OrderedDict()

	stopWords = []
	stopListFile = open("common_words", 'r')

	for word in stopListFile:
		stopWords.append(word.strip())

	print stopWords

	for line in rel_file:
		#print line
		#print "new---"
		p = line.split()
		k = p[0]
		temp = p[2][5:]
		#print k
		if k in rel_dict:
			rel_dict[k].append(temp)
		else:
			rel_dict[k] = []

			rel_dict[k].append(temp)	
	print rel_dict
	fr1= open("invertedindex_unigram.p","rb")
	uniIndex=pickle.load(fr1)
	#fr2= open('doctoID.p’,’r’)
	doc=pickle.load(open('doctoID.p','rb'))
	#fr3= open('tokenCount.p','r')
	docLen=pickle.load(open('tokenCount.p','rb'))
	#fr4= open('tokensInDoc.p','r')
	dcdt=pickle.load(open('tokensInDoc.p','rb'))
	length=len(doc)
	avdl=0
	k1=1.2
	k2=100
	b=0.25
	K={}




	def calc_avgdl(self):
		sum=0
		for d in self.docLen:
			sum=sum+self.docLen[d]
		self.avdl=sum/self.length
		#print(self.avdl)

	def calc_K(self):
		for d in self.docLen:
			a=self.b *(self.docLen[d]/self.avdl)
			self.K[d]= self.k1*((1-self.b)+a)

	def calc_score(self, query, qnum):
		score={}
		tokens1 = word_tokenize(query)
		tokens = []

		for word in tokens1:
			if word not in self.stopWords:
				tokens.append(word)

		print tokens

		#print tokens
		#tokens= query.split()
		for d in self.docLen:
			sum =0.0
			entry={}
			entry=self.dcdt[d]
			
			for term in tokens:
				ri = 0
				if term in self.uniIndex:
					ni=len(self.uniIndex[term])
					if term in entry:

						#ri = len((self.uniIndex[term].keys())&(self.rel_dict[qnum]))
						#print ri
						if str(qnum) not in self.rel_dict.keys():
							R= 0
							ri = 0
							
						else:		
							R = len(self.rel_dict[str(qnum)])

							for docid in self.uniIndex[term]:
							#print self.rel_dict['1']
								if str(docid) in self.rel_dict[str(qnum)]:
									ri = ri + 1
						#print str(qnum) + "rel of term -----" + str(ri)
						
						qi=tokens.count(term)
						fi=self.dcdt[d][term]
						s0=float((ri + 0.5)/(R - ri + 0.5))
						s1= float((ni-ri+0.5)/(self.length-ni-R+ri+0.5))
						s2=float(s0/s1)
						s3= float(((self.k1+1)*fi)/(self.K[d]+fi))
						s4=float(((self.k2+1)*qi)/(self.k2+qi))	

						s5= float(s2*s3*s4)
						#print s5
						if s5 <= 0:
							s6 = 0
						else:
							s6 = log(s5)	
					else:
						s6=0
					sum=sum+s6
			score[d]=sum
		return(score)

	def sortScore(self,dict1,num,fw):
		rank=0
		#t1 = PrettyTable(['Query_id','Literal','Doc_id : Doc_name','Rank','BM25_score','system_name'], border=True)
		fw.write('\n')
		
		for key, value in sorted(dict1.iteritems(), key=lambda (k,v): (v,k),reverse=True):
			rank=rank+1
			name = (k for k,v in self.doc.items() if v==key).next()
			#fw.write(str(num)+"    Q0    "+str(key)+" : "+str(name)+"   "+str(rank)+"      "+str(value)+" RAY ")
			if rank < 101:
				fw.write(str(num)+"\tQ0\t"+str(key)+" \t"+str(rank)+"\t"+str(value)+"\tRAY\t"+str(name))
				fw.write('\n')
				fw2.write(str(num)+" "+str(rank)+ " "+str(key)+" "+str(value))
				fw2.write('\n')
		fw.write('\n')



bm=BM25()
bm.calc_avgdl()
bm.calc_K()
file1='queries.txt'
fr=open(file1,'r')
file2='BM25Stoppedoutput.txt'
fw=open(file2,'w')

output_file = "BM25StoppedStats.txt"
fw2 = open(output_file,'w')

num=0
for line in fr:
	num=num+1
	fw.write("Query:"+line)
	query_text=line.strip('\n')
	query_text = query_text.lower()
	#print "query------" + str(query_text)
	s=bm.calc_score(query_text, num)
	#print(query_text)
	#print(s)
	bm.sortScore(s,num,fw)
