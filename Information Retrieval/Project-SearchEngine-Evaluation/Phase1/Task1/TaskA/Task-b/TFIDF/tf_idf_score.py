import pickle
import io
import os
import collections
from math import log
import math
from prettytable import PrettyTable
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")

class TFIDF:
	fr1= open("invertedindex_unigram.p","rb")
	uniIndex=pickle.load(fr1)
	doc=pickle.load(open('doctoID.p','rb'))
	docLen=pickle.load(open('tokenCount.p','rb'))
	dcdt=pickle.load(open('tokensInDoc.p','rb'))
	length=len(doc)
	tf_idf1={}
	


	def tf_idf_docs(self):
		docs=self.dcdt.keys()
		#print(docs)
		for d in docs:
			self.tf_idf1[d]={}
			entry={}
			entry=self.dcdt[d]
			for term in entry:
				if term in self.uniIndex:
					tf=float(self.dcdt[d][term])/float(self.docLen[d])
					idf= 1.0+float(log(float(self.length)/float(len(self.uniIndex[term]))))
					self.tf_idf1[d][term]=float(tf*idf)


	def tf_idf_query(self, query):
		tf_idf2={}
		tokens= query.split()
		docs=self.dcdt.keys()
		for d in docs:
			sum=0.0
			entry=self.dcdt[d]
			for term in tokens:
				if term in entry:
					sum=sum+self.tf_idf1[d][term]
			tf_idf2[d]=sum
		return tf_idf2

	def sortScore(self,dict1,num,fw,fw2):
		rank=0
		t1 = PrettyTable(['Query_id','Literal','Doc_id : Doc_name','Rank','TF_IDF_score','system_name'], border=True)
		fw.write('\n')

		
		for key, value in sorted(dict1.iteritems(), key=lambda (k,v): (v,k),reverse=True):
			rank=rank+1
			name = (k for k,v in self.doc.items() if v==key).next()
			#print(name)
			#print(value)
			if rank < 101:
				#t1.add_row(str(num)+" Q0 "+str(key)+" "+str(rank)+" "+str(value)+" RAY "+name)
				t1.add_row([num, 'Q0',str(str(key)+" : "+name[:-4]),rank,value,'RAY'])
				fw2.write(str(num)+" "+str(rank)+" "+str(key)+" "+str(value))
				fw2.write('\n')
		fw.write(t1.get_string())
		fw.write('\n')

file1='queries.txt'
fr=open(file1,'r')
file2='TFIDFRanking.txt'
fw=open(file2,'w')
file3='TFIDFStats.txt'
fw2=open(file3,'w')
#fw2.write("Qid Rank DocId Score")


num=0
a = TFIDF()
a.tf_idf_docs()
for line in fr:
	fw.write("Query:"+line)
	num=num+1
	query_text=line.strip('\n')
	q=a.tf_idf_query(query_text)
	a.sortScore(q,num,fw,fw2)

