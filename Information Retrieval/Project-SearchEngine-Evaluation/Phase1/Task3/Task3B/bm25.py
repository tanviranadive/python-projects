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
	
	rel_dict = OrderedDict([
		('1', ['1523', '2080', '2246', '2629', '3127']), 
		('2', ['115', '1223', '1231', '1551', '1625', '1795','1807', '1947', '2495','2579','2897']), 
		('3', ['141', '863', '950', '1601', '2266', '2664', '2714', '2973', '3075', '3156', '3175']), 
		('4', ['2578', '2849', '3137', '3148']), 
		('5', ['268', '1696', '1892', '2069', '2123', '2297', '2373', '2667','2862', '2970','2996','3078','3098']), 
		('6', ['268', '757', '963','1408','1518','1526','1533','1572','1653','1698','1719','1805','1892','1901','2085','2095','2218','2277','2318','2319','2358','2373','2434','2452','2535','2582','2667','2668','2669','2681','2741','2765','2798','2818','2831','2859','2862','2863','2881','2918','2928','2984','2988','2996','3006','3048','3059','3067','3088','3089','3119'])]) 
		

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
		tokens = word_tokenize(query)
		

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
		fw.write('\n')



bm=BM25()
bm.calc_avgdl()
bm.calc_K()
file1='queries.txt'
fr=open(file1,'r')
file2='BM25StemmedOutput.txt'
fw=open(file2,'w')

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
