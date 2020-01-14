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

def similar_text(reftext, text, embeddings, threshold):
    similar_para = []
    vector_1 = np.mean([embeddings[w] for w in reftext if w in embeddings], axis=0)
    for k, para in text.items():
        vector_2 = np.mean([embeddings[w] for w in para if w in embeddings], axis=0)
        print(1-calc_cosineSimilarity(vector_1, vector_2))
        if (1-calc_cosineSimilarity(vector_1, vector_2)) >= threshold:
            similar_para.append(k)
    
    return similar_para
