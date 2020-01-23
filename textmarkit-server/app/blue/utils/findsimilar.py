'''
    Version - 1.0
    Date - 14/01/2020
    
    Script function -
    This script consists of functions to find text similar to the favoritized text.
'''

from scipy.spatial import distance
import numpy as np
from collections import Counter

def calc_cosineSimilarity(v1, v2):
    return distance.cosine(v1, v2)

def similar_text(query, text, embeddings, threshold):
    similar_para = []
    vector_1 = np.mean([embeddings[w] for w in query if w in embeddings], axis=0)
    # vector_1 = np.sum([embeddings[w] for w in query if w in embeddings], axis=0)
    for k, para in text.items():
        vector_2 = np.mean([embeddings[w] for w in para if w in embeddings], axis=0)
        # vector_2 = np.sum([embeddings[w] for w in para if w in embeddings], axis=0)
        print(1-calc_cosineSimilarity(vector_1, vector_2))
        if (1-calc_cosineSimilarity(vector_1, vector_2)) >= threshold:
            similar_para.append(k)
    
    return similar_para

def similar_text2(query, embeddings, threshold):
    '''
        Find similarity between embeddings using cosine distance.

        Inputs - 
        query: embedding for the reference text
        embeddings: embeddings for text to be compared.
        threshold: threshold for similarity
    '''
    similar_para = []
    for i, embed in enumerate(embeddings):
        print(1-calc_cosineSimilarity(query, embed))
        if (1-calc_cosineSimilarity(query, embed))>=threshold:
            similar_para.append(i)
    
    print("similar para: ", similar_para)

    return similar_para

def similar_wmtext(query, text, threshold):
    '''
        Find similar text using pretrained word embeddings and Word Mover distance.
	
	Inputs - 
        query: reference text
        text: text corpus
        embeddings: dictionary of word embeddings.
        threshold: threshold for similarity
    '''
    similar_para = []

    from gensim.models import KeyedVectors
    model = KeyedVectors.load_word2vec_format('/content/gdrive/My Drive/GoogleNews-vectors-negative300.bin.gz', binary=True)

    query = query.split()
    for i, sen in enumerate(text):
        sen = sen.split()
        if (model.wmdistance(query, sen)) >= threshold:
            similar_para.append(i)

    print(similar_para)

    return similar_para

def cosine_similar_topk(query, embeddings, k=5):
    cosine_scores = []
    for i, embed in enumerate(embeddings):
        cosine_scores.append(1-calc_cosineSimilarity(query, embed))

    print(cosine_scores)

    print("Sorted: ", np.array(cosine_scores).argsort()[-k:])

    return np.array(cosine_scores).argsort()[-k:]
