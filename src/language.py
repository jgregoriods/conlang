import numpy as np

from .vocabulary import Vocabulary, SWADESH
from .utils import split_syllables, get_prob_dist


class Language:
    def __init__(self, phonemes, patterns, stress):
        self.phonemes = phonemes
        self.patterns = patterns
        self.stress = stress
        self.vocabulary = None
        self.rng = np.random.default_rng(42)

    def generate_word(self, pattern):
        res = ""
        for k in pattern:
            phoneme_probs = get_prob_dist(len(self.phonemes[k]))
            res += self.rng.choice(self.phonemes[k], p=phoneme_probs)
        syllables = split_syllables(res)
        stressed_syllable = self.rng.choice(self.stress)
        if stressed_syllable >= len(syllables):
            stressed_syllable = len(syllables) - 1
        for i, syllable in enumerate(syllables):
            if len(syllables) - i - 1 == stressed_syllable:
                syllables[i] = "'" + syllable
        return ''.join(syllables)

    def generate_vocabulary(self, adjust_length=True):
        vocabulary = Vocabulary(self)
        for i in SWADESH:
            if adjust_length and i[2] == 1:
                sel_patterns = [pattern for pattern in self.patterns if len(pattern) <= 3]
            else:
                sel_patterns = self.patterns
            pattern = self.rng.choice(sel_patterns)
            new_word = self.generate_word(pattern)
            attempts = 0
            while vocabulary.has_word(new_word):
                pattern = self.rng.choice(sel_patterns)
                new_word = self.generate_word(pattern)
                attempts += 1
                if attempts > 10:
                    print('Could not generate unique word, please check your parameters.')
                    break
            vocabulary.add_item(i[0], new_word)
        self.vocabulary = vocabulary
