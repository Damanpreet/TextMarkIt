'''
    Version - 1.0
    Date - 14/01/2020
    
    Script function -
    This script consists of functions to clean and preprocess the data before processing it.
'''
import string
import nltk
# nltk.download('stopwords') # to remove stopwords
# nltk.download('wordnet') # to lemmatize text
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

def preprocess_text1(text):
    '''
        Function to tokenize the data, remove punctuations and changing it into lower case.
    '''
    tokenizer = RegexpTokenizer(r'\w+')
    tokenized_sentence = tokenizer.tokenize(text.lower())
    # print("text: ", text)
    # print("********************")
    # print("tokenized sentence: ", tokenized_sentence)
    return tokenized_sentence
    
def remove_stopwords(text):
    '''
        Function to remove stop words. 
        Stop words are the most common words in english like the, a, an, are, as, for, from etc.
        
        Input: text with stop words
        Output: text without stop words.
    '''
    stopwords_set = set(stopwords.words('english'))
    filtered_text = " ".join([w for w in text if w not in stopwords_set])
    return filtered_text

def lemmatize_text(text):
    '''
        Function to lemmatize the input text.

    '''
    # instantiate lemmatizer -- do not instantiate for every line. check if you can pass this to the function.
    lemmatizer = WordNetLemmatizer()
    lem_text = [lemmatizer.lemmatize(w) for w in text]
    return lem_text

def stemming_text(text):
    '''
        Function to perform stemming of words.

        Stemming is the process to reduce the words to their root form.
    '''
    stemmer = PorterStemmer()
    stem_text = " ".join([stemmer.stem(w) for w in text])
    return stem_text

def preprocess_text(text):
    '''
        Function to preprocess the data.
        1. Tokenize the text
        2. Remove punctuations
        3. Change to lower case
        4. Remove stop words
        5. Lemmatization  
        6. Stemming

        Input - raw text
        Output - Preprocessed text
    '''
    text = preprocess_text1(text)
    text = remove_stopwords(text)
    # if uncommenting the below, be careful to modify stemming_text function.
    # text = lemmatize_text(text)
    # text = stemming_text(text)
    
    print(text)
    return text
