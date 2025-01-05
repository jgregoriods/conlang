import numpy as np

from .phonemes import COMMON_PHONEMES
from .utils import split_syllables
from .swadesh import SWADESH


MAX_ATTEMPTS = 10


def is_acceptable(word: str) -> bool:
    """
    Checks if the given word is acceptable.
    """

    # allow only one aspirated consonant
    if word.count('ʰ') > 1:
        return False

    # allow only one ejective consonant
    if word.count('ʼ') > 1:
        return False

    # allow only one long vowel
    if word.count('ː') > 1:
        return False

    # allow only one labialized consonant
    if word.count('ʷ') > 1:
        return False

    # prevent too many repeated characters
    if len(set(word)) < len(word) // 2:
        return False

    return True


def process_phonemes(phonemes: dict) -> dict:
    # we will cheat a bit to make the common phonemes more likely
    # to be chosen
    res = {}
    for k, v in phonemes.items():
        p = []
        for x in v:
            p.extend([x] * (2 if x in COMMON_PHONEMES else 1))
        res[k] = p
    return res


def generate_random_word(phonemes: dict, patterns: list, stress: list, idx: None) -> str:
    """
    Generates a random word based on the given phonemes, patterns and stress.
    """

    # the most frequent words are more likely to be shorter
    if idx is not None and idx < 25:
        pattern = np.random.choice(patterns[:2])
    else:
        pattern = np.random.choice(patterns)

    res = ''
    for k in pattern:
        res += np.random.choice(phonemes[k])

    syllables = split_syllables(res)

    stressed = max(np.random.choice(stress), -len(syllables))
    syllables[stressed] = "ˈ" + syllables[stressed]

    word = ''.join(syllables)

    return word


def generate_random_vocabulary(phonemes: dict, patterns: list, stress: list, glosses: list) -> dict:
    """
    Generates a random vocabulary based on the given phonemes, patterns, stress and glosses.
    """
    vocabulary = {}
    glosses = glosses or SWADESH
    patterns = sorted(patterns, key=len)
    phonemes = process_phonemes(phonemes)
    for gloss in glosses:
        idx = SWADESH.index(gloss) if gloss in SWADESH else None
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            word = generate_random_word(phonemes, patterns, stress, idx)
            if is_acceptable(word) and word not in vocabulary.values():
                break
            attempts += 1
        vocabulary[gloss] = word
    return vocabulary
