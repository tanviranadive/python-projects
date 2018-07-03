# Task 1: To clean the corpus

from CorpusCleaner import Cleaner

# directory from where the raw corpus is taken
inputrootdir = "/Users/Shraddha/Desktop/IR-Project/cacm/"

# directory where the cleaned and stopped corpus is stored
outrootdir = "cacm/"

stopWords = []
stopListFile = open("common_words", 'r')

for word in stopListFile:
	stopWords.append(word.strip())

clean = Cleaner()

clean.getCleanCorpus(inputrootdir, outrootdir, stopWords)