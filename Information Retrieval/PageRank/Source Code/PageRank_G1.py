from collections import OrderedDict

import re
import sys
import codecs
reload(sys)
from urlparse import urljoin
sys.setdefaultencoding('utf-8')
import math
import operator

perplexityList = []
newPR = OrderedDict()

def main():		

	
	file1 = open('CrawlerGraph1.txt', 'r')

	#Create list of pages P and list of sinknodes
	P = []
	sinknodes =[]

	#create an ordered dictionary for M which represents the inlinks for each key in M
	M = OrderedDict()
	for line in file1:
		line = line.strip().split(" ")
		M[line[0]]= set(line[1:])
		
	#Initializing the pages list with the keys in M to get all the pages
	for key in M:
		#print M[key]
		P.append(key)
	#print P	

	#create an ordered dictionary for L which represents the number of outlinks for each page
	# and initialize it to 0. Increment the count of the number of outlinks for each page 
	# when that page is encountered in the inlinks graph

	L = OrderedDict()
	for key in M:
		L[key] = 0

	for key in M:
		for u in M[key]:
			L[u] = L[u] + 1

	#Create a list of sink nodes S and add the page into S if corresponding page does not have 
	# any outlinks i.e L[key] = 0

	S = []

	for key in L:
		if L[key] == 0:
			#print "appending in S"
			S.append(key)

	print "Sink nodes:----"	
	print len(S)	
	#print S		

	#List of pages with no inlinks. Add the page into the list if M[key] does not have any inlinks
	NoInlinks = []

	for key in M:
		if len(M[key]) == 0:
			NoInlinks.append(key)

	print "Pages with no inlinks: "
	print len(NoInlinks)
	#print NoInlinks

	d = 0.85
	n = len(P)
	print "Number of total links :" + str(n)

	#Create ordered dictionary for PageRank of each page and initialize it to 1/n

	PR = OrderedDict()
	for key in P:
		PR[key] = 1/float(n)

	#calculate perplexity initially
	print "Iteration 0"
	t = calculateperplexity(PR,n)

		
	# call the pagerank function to calculate page rank
	pagerank(P,PR,M,L,n,S,d)
	#print PR

	# Sort the PageRank dictionary according to the value of their pagerank 
	# in descending order

	sortedPR = sorted(PR.items(), key=operator.itemgetter(1), reverse = True)
	print "sorted PR:"
	#print sortedPR
	
	c=0
	print "First 50 pages"
	while c<50 :
		print (sortedPR[c])
		c= c+1
	
	# create ordered dictionary inlinkcount to store the number of inlinks for each page
	# and sort it from high to low
	inlinkcount = OrderedDict()
	for p in M:
		lenp = len(M[p])
		inlinkcount[p] = lenp
	sortedInlinkCount = sorted(inlinkcount.items(), key=operator.itemgetter(1), reverse = True)
	print "Inlinks count sorted"
	print sortedInlinkCount

# define function to calculate perplexity value	
def calculateperplexity(PR,n):
	
	h = 0
	for key in PR:
		h = h + (PR[key]*((math.log(PR[key]))/(math.log(2))))
		
	perplexity = 2 ** (-h)	
	print "Perplexity ----" +str(perplexity)
	perplexityList.append(perplexity)	


	
# define function to calculate page rank till convergence not reached		
def pagerank(P,PR,M,L,n,S,d):
	
	i=0
	
	while (calculateconvergence(i)):
		sinkPR = 0

		#calculate total sink PR
		for p in S:
			sinkPR = sinkPR + PR[p]

			
		for p in P:
			#Teleportation
			newPR[p] = float((1-d))/float(n)

			# spread remaining sinkPR evenly
			newPR[p] = newPR[p] + (d*(float(sinkPR)/n))

			#Add share of page rank from inlinks
			for q in M[p]:
				newPR[p] = newPR[p] + d*(float(PR[q])/float(L[q]))
		for p in P:
			PR[p] = newPR[p]
		#print PR	
		print "Iteration " + str(i+1)
		
		temp = calculateperplexity(PR,n)

		i = i + 1	

# define function to calculate convergence
def calculateconvergence(i):
	if i < 4:
		return True
	else:
		temp = i
		while temp > (i-4):
			if abs(perplexityList[temp] - perplexityList[temp-1]) < 1:
				temp = temp-1
				continue
			else:
				return True	
		return False



if __name__== '__main__':
    main()    



