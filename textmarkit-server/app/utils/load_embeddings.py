import numpy as np

wordembed="data/glove.6B/glove.6B.50d.txt"
def load_gloveEmbeddings():
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
