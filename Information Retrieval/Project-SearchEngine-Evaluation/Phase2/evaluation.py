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

class Evaluation:
	file3 = open("MAP_and_MRR.txt",'a')
	file4 = open("P@K.txt", "a")


	relevanceJudgement = pickle.load(open("cacm_rel_dict.txt","rb"))
	print relevanceJudgement

	def getStats(self, filename1,filename2):
		file=open(filename1,'r')
		file2=open(filename2,'w')
		self.file4.write("P@K for" + filename1)
		self.file4.write("\n")
		AvgPrecisionSet=[]
		MRR=[]
		sum = 0
		rel = 0
		avgPrecison = 0
		for line in file:
			tokens=line.split()
			queryId=int(tokens[0])
			rank=int(tokens[1])
			if rank==1:
				rel=0
				sum=0
				avgPrecison = 0
			docId=int(tokens[2])
			file2.write(line.strip())
			# print(queryId)
			# print(rank)
			# print(docId)
			if queryId in self.relevanceJudgement:
				l=len(self.relevanceJudgement[queryId])
				if docId in self.relevanceJudgement[queryId]:
					#document is relevant
					file2.write(" 1 ")
					rel=rel+1
					if rel ==1:
						MRR.append(float(1)/rank)
					precision=float(rel)/rank
					sum=sum+precision
				else:
					file2.write(" 0 ")
					precision=float(rel)/rank
				recall=float(rel)/l
				file2.write(str(precision)+" "+str(recall))
				file2.write('\n')
				if rank == 5:
					self.file4.write("QueryId: " + str(queryId))
					self.file4.write("\n")
					self.file4.write("P@" + str(rank) + " " + " : " + str(precision) + "   ")
				if rank == 20:
					self.file4.write("P@" + str(rank) + " " + " : " + str(precision)) 
					self.file4.write("\n")

				if rank==100:
					if rel==0:
						avgPrecison=0
					else:
						avgPrecison=float(sum)/rel
					AvgPrecisionSet.append(avgPrecison)

		if rel==0:
			avgPrecison=0
		else:
			avgPrecison=float(sum)/rel
		AvgPrecisionSet.append(avgPrecison)
		mean=0.0
		for val in AvgPrecisionSet:
			mean=mean+val
		MAP=float(mean)/len(AvgPrecisionSet)
		mean=0.0
		for val in MRR:
			mean=mean+val
		mrr=float(mean)/len(MRR)
		self.file3.write(filename1+ "MAP -> "+str(MAP))
		self.file3.write("\n")
		self.file3.write(filename1+ "MRR -> "+str(mrr))
		self.file3.write("\n")
		self.file4.write("\n")
		


a = Evaluation()

a.getStats("BM25ExpandedQueryStats.txt","BM25ExpandedQuery_Precision&Recall.txt")
a.getStats("BM25Stats.txt","BM25_Precision&Recall.txt")
a.getStats("LuceneStats.txt","Lucene_Precision&Recall.txt")
a.getStats("VSMStoppedStats.txt","VSMStopped_Precision&Recall.txt")
a.getStats("VSMStats.txt","VSM_Precision&Recall.txt")
a.getStats("BM25StoppedStats.txt","BM25Stopped_Precision&Recall.txt")
a.getStats("TFIDFStats.txt","TFIDF_Precision&Recall.txt")


#file3.write("VSMStats.txt "+str(MAP))




