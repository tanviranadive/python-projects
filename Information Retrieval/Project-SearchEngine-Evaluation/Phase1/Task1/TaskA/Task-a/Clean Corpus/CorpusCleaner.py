__author__ = 'shraddha shah'

#class to clean(parse and tokenize) the corpus

import os
import nltk
from nltk import word_tokenize
from bs4 import BeautifulSoup
from bs4 import Comment
import sys
import string
from collections import OrderedDict
import re
import io
reload(sys)
sys.setdefaultencoding('utf8')

class Cleaner:

	punctuation = '!"#&$%' + "'()*+;<=>?@[]^_`{|}~'\/"
	articles = []
	i = 1


	def getCleanCorpus(self, inputrootdir, outrootdir):
		""" input  : directory of the raw corpus
					 directory where we will store the cleaned corpus
			output : cleaned(parsed and tokenized) articles 
		"""

		rootdir = inputrootdir
		for file in os.listdir(rootdir):
			if (file != '.DS_Store'):
				raw_text = self.parseCorpus(inputrootdir,file)
				self.tokenzieCorpus(outrootdir,raw_text,file)


	def parseCorpus(self,inputrootdir,file):
		""" input  : directory of the raw corpus
					 file(article) to be cleaned
			output : parsed article of the given article
		"""
		
		doc = open(inputrootdir + file)

		soup = (BeautifulSoup(doc)).find('pre')


		

		raw_text = soup.text.lower()
		raw_text = ''.join(c for c in raw_text if c not in self.punctuation)
		
		raw_text=raw_text.replace("-"," ")
		raw_text=raw_text.replace(":"," ")
		raw_text=raw_text.replace(","," ")
		raw_text=raw_text.replace("."," ")

		
		return raw_text


	def tokenzieCorpus(self,outrootdir,raw_text,file):
		""" input  : directory where we will store the cleaned corpus
					 parsed file of the article
					 name of the file
			output : tokenized file of the article
		"""
		
		print(file)
		
		tokens = word_tokenize(raw_text)
		with open(outrootdir + file,'w') as f:
			for token in tokens:
				f.write(token + " ")



    
