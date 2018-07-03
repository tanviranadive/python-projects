# to build a retrieval module using Vector Space Cosine Similarity Ranking Algorithm
import pickle

from RetrievalModule import Ranker

queries = open("queries.txt", 'r')
ranks = Ranker()
ranks.getRankedDocuments(queries)

