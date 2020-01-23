'''
    Version - 1.0
    Date - 14/01/2020
    
    Script function -
    This script consists of functions to load word embeddings.
'''

import numpy as np

wordembed="data/glove.6B/glove.6B.300d.txt"
def load_gloveEmbeddings():
    '''
        Function to load pretrained glove word embeddings.
    '''
    print("Loading the GloVe Embeddings")
    model = {}
    data = open(wordembed, encoding='utf8').readlines()
    for line in data:
        linespl = line.split()
        word = linespl[0]
        embeddings = np.array([float(val) for val in linespl[1:]])
        model[word] = embeddings
    
    print("Completed! {} words loaded.".format(len(model)))
    return model

def load_fastTextEmbeddings(data):
    import fastText
    # download the model for english language
    fastText.util.download_model('en', if_exists='ignore')
    ft = fastText.load_model('cc.en.300.bin')
    model={}
    for line in data:
        for word in line:
            model[word]=ft.get_word_vector(word)
    
    print("Completed! fastText Embeddings loaded for {} words.".format(len(model)))

    return model

def load_elmoEmbeddings(data):
    '''
        Function to load Elmo word embeddings.
    '''

    print("Loading Elmo embeddings.")
    import os
    os.environ['CUDA_VISIBLE_DEVICES']='2'

    import tensorflow as tf
    import tensorflow_hub as hub
    elmo = hub.Module("https://tfhub.dev/google/elmo/2", trainable=True)
    embeddings = elmo(data, signature='default', as_dict='True')['elmo']
    
    print("Embeddings loaded successfully.")

    init = tf.initialize_all_variables()
    sess = tf.Session()
    sess.run(init)

    model = {}
    c=1
    for line in data:
        for i in range(len(line)):
            model[line[i]]=sess.run(embeddings[0][i])
        print("Ran for {} sentence".format(c))
        c+=1

    return model


def load_sentenceEmbeddings(data):
    '''
        Function to load pretrained sentence embeddings using the model Universal Sentence Encoder.

        Input: input data
        Output: Embeddings for sentences
    '''

    import os
    import tensorflow as tf
    import tensorflow_hub as hub

    device_name  = tf.test.gpu_device_name()
    if device_name=='/device:GPU:0':
        os.environ['CUDA_VISIBLE_DEVICES']='0'
    
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4" #@param ["https://tfhub.dev/google/universal-sentence-encoder/4", "https://tfhub.dev/google/universal-sentence-encoder-large/5"]
    model = hub.load(module_url)

    def embed(input):
        return model(input)

    embeddings = embed(data)
    
    return embeddings
