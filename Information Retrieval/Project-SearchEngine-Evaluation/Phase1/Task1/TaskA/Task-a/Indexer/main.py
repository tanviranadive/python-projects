# to create inverted index for the given corpus

from Indexer import IndexCreator

rootdir = "/Users/Shraddha/Desktop/IR-Project/cleaned_cacm/"


index = IndexCreator()
index.docToID(rootdir)

invertedIndex = index.getIndex(rootdir, 1)

# invertedIndex = index.getIndex(rootdir, 2)
# invertedIndex = index.getIndex(rootdir, 3)

# to get the count of tokens in each of the document
tokenCount = index.getTokensInADoc()
tokensDoc = index.getTokens()

# to get the index and the document statistics
index.dumpIndex(invertedIndex,1)
index.storeDocStatistics(invertedIndex,1)

# index.dumpIndex(invertedIndex,2)
# index.storeDocStatistics(invertedIndex,2)

# index.dumpIndex(invertedIndex,3)
# index.storeDocStatistics(invertedIndex,3)
