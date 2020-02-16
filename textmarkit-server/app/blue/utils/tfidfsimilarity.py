from app.blue.utils.preprocess import preprocess_text 
from collections import defaultdict
from app.blue.utils import tfidf_utils

def tfidf_similartext(data, file_format):
    testdata = {}
    corpus = set()
    DF = defaultdict(lambda: 0)
    
    if file_format=='txt':               
        for c, row in enumerate(data):
            if len(row)>0:
                testdata[c]=preprocess_text(" ".join(row.split("\n"))) # preprocess the data
                tokens = set(testdata[c].split())
                corpus.update(tokens) # update the set of vocab
                for w in tokens:
                    DF[w]+=1
    elif file_format=='csv':
        c=0
        csv_reader = csv.reader(data, delimiter=',', quotechar='"')
        for row in csv_reader:
            if len(row)>0:
                testdata[c]=preprocess_text(" ".join(row[0].split("\n"))) # preprocess the data
                tokens = set(testdata[c].split())
                corpus.update(tokens) # update the set of vocab
                for w in tokens:
                    DF[w]+=1
                c+=1

    embeddings = tfidf_utils.calc_tfidf(list(testdata.values()), list(corpus), DF)
    
    return embeddings