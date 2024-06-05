import numpy as np


VOWELS = ["a", "e", "i", "o", "u"]


def split_syllables(word):
    i, j = 0, 0
    res = []
    while j < len(word):
        if word[j] in VOWELS:
            res.append(word[i:j+1])
            i = j + 1
        j += 1
    if i < len(word):
        res[-1] += word[i:]
    return res


def get_prob_dist(length, decay=0.2):
    ranks = np.arange(1, length + 1)
    probs = np.exp(-decay * (ranks - 1))
    probs /= np.sum(probs)
    return probs
