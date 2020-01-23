import load_embeddings
from preprocess import preprocess_text # for tf-idf
import findsimilar
import csv
import io
threshold = 0.2 # configuration to determine the similarity.
from collections import defaultdict
import tfidf_utils

if __name__ == "__main__":
    testdata = {}
    corpus = set() # for tf-idf

    c = 0 
    DF = defaultdict(lambda: 0)
    with open('testdata.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        for row in csv_reader:
            if len(row)>0:
                # testdata[c] =" ".join(row[0].split("\n")) # strip "\n"
                testdata[c]=preprocess_text(" ".join(row[0].split("\n"))) # preprocess the data
                tokens = set(testdata[c].split())
                corpus.update(tokens) # update the set of vocab
                for w in tokens:
                    DF[w]+=1
                c+=1

    # c=0
    # vocab={}
    # for w in corpus:
    #     vocab[w]=c
    #     c+=1 

    embeddings = tfidf_utils.calc_tfidf(list(testdata.values()), list(corpus), DF)
    similarity_list = findsimilar.cosine_similar_topk(embeddings[0], embeddings[1:], 3)

    # embeddings = load_embeddings.load_sentenceEmbeddings(list(testdata.values()))

    # similarity_list = findsimilar.similar_text2(embeddings[0], embeddings, threshold)
    # similarity_list = findsimilar.similar_wmtext(testdata[0], testdata, embeddings, threshold)

    print("paragraphs similar to the reference text: ",)
    for p in similarity_list:
        print(testdata[p])
        print()
