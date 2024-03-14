# utils.py
import nltk
from nltk.corpus import wordnet
import random

nltk.download('wordnet')

def get_all_words():
    all_words = set()
    for synset in list(wordnet.all_synsets()):
        all_words.update(lemma.name() for lemma in synset.lemmas())
    return all_words

def is_valid_word(word, used_words, last_letter):
    return word not in used_words and word.startswith(last_letter)

def get_random_starting_player(players):
    return random.choice(players)