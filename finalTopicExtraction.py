import pickle
import gensim
from gensim import corpora
from stop_words import get_stop_words
import spacy
from spacy.lang.en import English
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
spacy.load('en')
parser = English()


def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens


def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma
    

def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)


def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    en_stop = set(get_stop_words('en'))
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens


text_data = []
documents = []
for i in range(0,50):
    try:
        with open('data/video' + str(i+1) + '.txt', 'r') as myfile:
            data=myfile.read().replace('\n', '')
        data = data.replace('%HESITATION', '')
        documents.append(data)
        tokens = prepare_text_for_lda(data)
        text_data.append(tokens)
    except:
        pass
        

dictionary = corpora.Dictionary(text_data)
corpus = [dictionary.doc2bow(text) for text in text_data]

pickle.dump(corpus, open('corpus.pkl', 'wb'))
dictionary.save('dictionary.gensim')


NUM_TOPICS = 5
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
ldamodel.save('model5.gensim')
topics = ldamodel.print_topics(num_words=4)
for topic in topics:
    print(topic)

for i in range(0,50):
    try:
        new_doc = documents[i]
        new_doc = prepare_text_for_lda(new_doc)
        new_doc_bow = dictionary.doc2bow(new_doc)
        print('Video' + str(i+1) + ':')
        print(ldamodel.get_document_topics(new_doc_bow))
    except:
        pass