import numpy as np

from .utils import split_syllables


def generate_random_word(phonemes: dict, patterns: list, stress: list) -> str:
    """
    Generates a random word based on the given phonemes, patterns and stress.
    """
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
    for gloss in glosses:
        vocabulary[gloss] = generate_random_word(phonemes, patterns, stress)
    return vocabulary
