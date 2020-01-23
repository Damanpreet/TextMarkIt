# import app.blue.utils.load_embeddings
from app.blue.utils.preprocess import preprocess_text # for tf-idf
import app.blue.utils.findsimilar
import csv
import io
from collections import defaultdict
import app.blue.utils.tfidf_utils

threshold = 0.2 # configuration to determine the similarity.
def tfidf_similartext(csv_data):
    testdata = {}
    corpus = set()
    c = 0 
    DF = defaultdict(lambda: 0)
    
    csv_reader = csv.reader(csv_data, delimiter=',', quotechar='"')
    for row in csv_reader:
        if len(row)>0:
            testdata[c]=preprocess_text(" ".join(row[0].split("\n"))) # preprocess the data
            tokens = set(testdata[c].split())
            corpus.update(tokens) # update the set of vocab
            for w in tokens:
                DF[w]+=1
            c+=1

    embeddings = tfidf_utils.calc_tfidf(list(testdata.values()), list(corpus), DF)
    similarity_list = findsimilar.cosine_similar_topk(embeddings[0], embeddings[1:], 3)

    print("paragraphs similar to the reference text: ",)
    for p in similarity_list:
        print(testdata[p])
        print()
    
    return similarity_list