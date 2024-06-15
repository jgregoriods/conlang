import numpy as np
import re

from .phonemes import VOWELS, SEMIVOWELS, PHONEMES, SUPRASEGMENTALS


def split_syllables(word):
    i, j = 0, 0
    res = []
    while j < len(word):
        if word[j] in VOWELS:
            if j < len(word) - 1 and word[j+1] == ':':
                pass
            else:
                if j < len(word) - 1 and word[j+1] in SEMIVOWELS:
                    if j + 2 < len(word) and word[j+2] in VOWELS:
                        res.append(word[i:j+1])
                        i = j + 1
                    else:
                        res.append(word[i:j+2])
                        i = j + 2
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


def mark_wildcards(word, wildcards):
    phonemes = split_phonemes(word)
    for k, v in wildcards.items():
        for i, phoneme in enumerate(phonemes):
            if phoneme in v:
                phonemes[i] = f"{k} {phoneme} {k}"
    new_word = ' '.join(phonemes)
    for k in wildcards:
        new_word = new_word.replace(f"{k} '", f"' {k}")
    return new_word


def multiple_replace(word, rule):
    repl_dict = {f" {k} ":f" {v} " for k,v in rule['rules'].items()}
    if 'wildcards' in rule:
        phonemes = mark_wildcards(word, rule['wildcards'])
    else:
        phoneme_list = split_phonemes(word)
        phonemes = f" {' '.join(phoneme_list)} "
    regex = re.compile('|'.join(map(re.escape, repl_dict.keys())))
    new_phonemes = re.sub(regex, lambda match: repl_dict[match.group(0)], phonemes)

    if 'wildcards' in rule:
        regex = re.compile('|'.join(k for k in rule['wildcards']))
        new_phonemes = re.sub(regex, '', new_phonemes)

    return new_phonemes.replace(' ', '')

