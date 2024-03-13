# utils.py
import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')

def get_all_words():
    all_words = set()
    for synset in list(wordnet.all_synsets()):
        all_words.update(lemma.name() for lemma in synset.lemmas())
    return all_words
