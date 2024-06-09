import numpy as np

from .phonemes import VOWELS, PHONEMES, SUPRASEGMENTALS


def split_syllables(word):
    i, j = 0, 0
    res = []
    while j < len(word):
        if word[j] in VOWELS:
            if j < len(word) - 1 and word[j+1] == ':':
                pass
            else:
                res.append(word[i:j+1])
                i = j + 1
        elif word[j] == ':':
            res.append(word[i:j+1])
            i = j + 1
        j += 1
    if i < len(word):
        res[-1] += word[i:]
    return res


def split_phonemes(word):
    res = []
    i = 0
    while i < len(word):
        if word[i:i+3] in list(PHONEMES) + SUPRASEGMENTALS:
            res.append(word[i:i+3])
            i += 3
        elif word[i:i+2] in list(PHONEMES) + SUPRASEGMENTALS:
            res.append(word[i:i+2])
            i += 2
        else:
            res.append(word[i])
            i += 1
    return res


def get_prob_dist(length, decay=0.2):
    ranks = np.arange(1, length + 1)
    probs = np.exp(-decay * (ranks - 1))
    probs /= np.sum(probs)
    return probs
