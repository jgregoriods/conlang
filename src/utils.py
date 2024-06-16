import numpy as np
import re
from .phonemes import CONSONANTS, VOWELS, SEMIVOWELS, PHONEMES, SUPRASEGMENTALS


def split_phonemes(word: str) -> list:
    phonemes = list(PHONEMES) + SUPRASEGMENTALS
    result = []
    i = 0
    while i < len(word):
        for length in (3, 2, 1):
            if word[i:i+length] in phonemes:
                result.append(word[i:i+length])
                i += length
                break
    return result


def split_syllables(word: str) -> list:
    phonemes = split_phonemes(word)
    syllables = []
    start = 0

    for i, phoneme in enumerate(phonemes):
        if phoneme in VOWELS:
            end = i + 1
            if i + 1 < len(phonemes) - 1 and phonemes[i + 1] in SEMIVOWELS:
                end = i + 2
            syllables.append(phonemes[start:end])
            start = end

    # Append the last syllable if there are any phonemes left
    if start < len(phonemes):
        remaining_phonemes = phonemes[start:]
        if not set(remaining_phonemes).intersection(VOWELS):
            syllables[-1] += remaining_phonemes
        else:
            syllables.append(phonemes[start:])

    # This is a quick fix to split consonant clusters by moving the first consonant to the previous syllable
    for i in range(1, len(syllables)):
        if len(syllables[i]) > 1 and syllables[i][0] in CONSONANTS and syllables[i][1] in CONSONANTS:
            syllables[i-1] += syllables[i][0]
            syllables[i] = syllables[i][1:]

    return [''.join(syllable) for syllable in syllables]


def get_prob_dist(length: int, decay: float = 0.2) -> np.ndarray:
    ranks = np.arange(1, length + 1)
    probs = np.exp(-decay * (ranks - 1))
    probs /= np.sum(probs)
    return probs


def mark_wildcards(word: str, wildcards: dict) -> str:
    phonemes = split_phonemes(word)
    for k, v in wildcards.items():
        for i, phoneme in enumerate(phonemes):
            if phoneme in v:
                phonemes[i] = f"{k} {phoneme} {k}"
    new_word = ' '.join(phonemes)
    for k in wildcards:
        new_word = new_word.replace(f"{k} '", f"' {k}")
    return new_word


def multiple_replace(word: str, rule: dict) -> str:
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

