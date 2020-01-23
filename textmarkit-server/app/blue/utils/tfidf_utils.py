'''
    Version - 1.0
    Date - 16/01/2020
    
    Script function -
    This script consists of functions to calculate the tf idf of text.
'''

import numpy as np
from collections import Counter

INVALID_INPS_FREQ = "Error while calculating the frequency distribution. Check inputs."
INVALID_FREQ_DISTR = "Error while calculating frequency distribution of words."
ERR_TFIDF = "Error while calculating TF-IDF score."
ERR_TFIDF_SC = "Error in the outer block while calculating the TF-IDF score."

def calc_df(input_paras, word):
    '''
        Calculate df (document frequency) of a word.
        
        Input-
        word: 

        Output-
        returns the document frequency of word
    '''
    c=0
    for inp in input_paras:
        if word in inp:
            c+=1
    
    return c

def calc_tfidf(input_paras, vocab, DF):
    '''
        Function to calculate the tf-idf score.

        Inputs -
        input_paras:
        vocab:

        Output-

    '''
    try:
        N = len(input_paras)
        V = len(vocab)
        if N==0 or V==0:
            raise ValueError(INVALID_INPS_FREQ)

        tf_idf = dict()
        for i in range(N):
            counter = Counter(input_paras[i].split())
            words_count = len(counter)

            for w, val in counter.items():
                tf = val/words_count
                df = DF[w] #calc_df(input_paras, w)
                idf = np.log((N+1))/(df+1)
                tf_idf[i, w] = tf*idf
        
        tfidf = np.zeros((N, V))

        try:
            for tup in tf_idf:
                inds = vocab.index(tup[1])
                tfidf[tup[0]][inds] = tf_idf[tup]
        except:
            raise ValueError(ERR_TFIDF)    
        return tfidf 
    except:
        raise ValueError(ERR_TFIDF_SC)

def calc_frequency_distr(input_paras, vocab):
    '''
        Function to calculate the frequency distribution of words in a paragraph.

        Inputs-
        input_paras:
        vocab:

        Outputs-
        returns 
    '''
    if len(input_paras)==0 or len(vocab)==0:
        raise ValueError(INVALID_INPS_FREQ)

    try:
        p = len(input_paras)
        freq_distr = np.zeros((p, len(vocab)))
        for i in range(p):
            counter = Counter(input_paras[i].split())
            for w in counter:
                freq_distr[i, vocab[w]]=counter[w]
        return freq_distr
    except:
        raise ValueError(INVALID_FREQ_DISTR)
