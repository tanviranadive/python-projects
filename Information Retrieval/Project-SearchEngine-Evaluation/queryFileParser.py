# to parse the cacm.query to get the queries in a line by line format 

from bs4 import BeautifulSoup
import pickle
import collections

queryFile = open("cacm.query")
parsedFile = BeautifulSoup(queryFile)
parsedQueryFile = open("queries.txt", 'w')

punctuation = '!"#&$%' + "'()*+;<=>?@[]^_`{|}~'\/"

# Dictionary to save query id and the query
queryDict = collections.OrderedDict()

i = 1

for query in (parsedFile.findAll("doc")):
	for line in query:
		line = str(line)
		if line[0:7] != "<docno>" and line[0:2] != '\n':
			line = line.replace('\n','  ')
			line = line.replace('\t','  ')
			line = ''.join(c for c in line if c not in punctuation)
			line = line.replace("-"," ")
			line = line.replace(":"," ")
			line = line.replace(","," ")
			line = line.replace("."," ")
			line = line.lower()
			parsedQueryFile.write(line.strip())
			parsedQueryFile.write('\n')
			queryDict[i] = line.strip()
			i = i + 1

with open("queryIDDict.txt", 'wb') as file:
	pickle.dump(queryDict, file)




