import numpy as np

from .phonemes import VOWELS


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


# will be changed to account for phonemes
# that have more than one character
def split_phonemes(word):
    return list(word)


def get_prob_dist(length, decay=0.2):
    ranks = np.arange(1, length + 1)
    probs = np.exp(-decay * (ranks - 1))
    probs /= np.sum(probs)
    return probs
