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

    return similar_para

def cosine_similar_topk(query_id, query, embeddings, k=6):
    '''
        Find top k similar paragraphs using cosine similarity.
    '''
    try:
        cosine_scores = []
        for i, embed in enumerate(embeddings):
            cosine_scores.append(1-calc_cosineSimilarity(query, embed))

        top_ksimilar = np.array(cosine_scores).argsort()[-k:].tolist()
        top_ksimilar = [x+1 for x in top_ksimilar]

        print("removing the query id from the similarity array.")
        print(top_ksimilar, query_id)

        if query_id in top_ksimilar:
            top_ksimilar.remove(query_id)
            print("removed the query id. updated: ", top_ksimilar)
        
        return top_ksimilar

    except Exception as e:
        print("Error while finding the similarity of paragraphs.")
        print("Error: ", e)
        return []

def cosine_similar(query_id, query, embeddings, threshold):
    '''
        Function to find similar paragraphs based on cosine similarity between paragraphs.
    '''
    try:
        cosine_scores = []
        for i, embed in enumerate(embeddings):
            cosine_scores.append(1-calc_cosineSimilarity(query, embed))

        print(cosine_scores)
        top_ksimilar = np.nonzero(np.array(cosine_scores) > threshold)[0].tolist()
        top_ksimilar = [x+1 for x in top_ksimilar]

        print("removing the query id from the similarity array.")
        print(top_ksimilar, query_id)

        if query_id in top_ksimilar:
            top_ksimilar.remove(query_id)
            print("removed the query id. updated: ", top_ksimilar)

        return top_ksimilar
    except Exception as e:
        print("Error while finding the similarity of paragraphs.")
        print("Error: ", e)
        return []