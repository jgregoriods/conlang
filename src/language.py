import numpy as np
import warnings
import json
import uuid

from .sound_change import SoundChange
from .vocabulary import Vocabulary, SWADESH
from .utils import split_syllables, get_prob_dist


VALID_MORPHOLOGIES = {'agglutinative', 'fusional', 'isolating', 'polysynthetic'}
VALID_POS = {'S', 'O', 'V'}
MAX_ATTEMPTS = 100


def is_acceptable(word: str, ratio: float = 0.67) -> bool:
    # for short words we are more lenient
    if len(word) < 3:
        return True

    # avoid too many long vowels or aspirations
    for char in [":", "ʰ"]:
        if word.count(char) > 1:
            return False

    # avoid ending in aspiration
    if word[-1] in ['ʰ']:
        return False

    # avoid repetitive phonemes
    if len(set(word)) / len(word) < ratio:
        return False

    return True


class Language:
    def __init__(self, phonemes: dict, patterns: list, stress: list,
                 morphology: str = 'fusional', word_order: str = 'SVO',
                 id: str = ''):
        self.phonemes = phonemes
        self.patterns = patterns
        self.stress = stress
        self.vocabulary = None
        self.rng = np.random.default_rng()
        self.id = id if id else str(uuid.uuid4())

        if morphology not in VALID_MORPHOLOGIES:
            raise ValueError(f'Invalid morphology type: {morphology}. Must be one of {VALID_MORPHOLOGIES}.')
        self.morphology = morphology
        
        if len(word_order) != 3 or set(word_order) != VALID_POS:
            raise ValueError(f'Invalid word order: {word_order}. Must be a permutation of {VALID_POS}.')
        self.word_order = word_order

    def generate_word(self, pattern: str = '') -> str:
        if not pattern:
            pattern = self.rng.choice(self.patterns)

        res = ''

        # phonemes are not chosen uniformly, but according to a distribution
        # based on the order of appearance in the phoneme list
        for k in pattern.split():
            phoneme_probs = get_prob_dist(len(self.phonemes[k]))
            res += self.rng.choice(self.phonemes[k], p=phoneme_probs)

        syllables = split_syllables(res)
        stressed_syllable = max(self.rng.choice(self.stress), -len(syllables))
        syllables[stressed_syllable] = "'" + syllables[stressed_syllable]

        return ''.join(syllables)

    def generate_vocabulary(self, adjust_length: bool = True):
        self.vocabulary = Vocabulary(self.id)
        for item in SWADESH:
            # if adjust_length is True, the most frequent words will be shorter
            sel_patterns = [pattern for pattern in self.patterns if len(pattern) <= 3] if adjust_length and item[2] == 1 else self.patterns
            new_word = self._generate_unique_word(sel_patterns)
            self.vocabulary.add_item(item[0], new_word)
    
    def _generate_unique_word(self, patterns: list = list()) -> str:
        if not patterns:
            patterns = self.patterns
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            pattern = self.rng.choice(patterns)
            new_word = self.generate_word(pattern)
            if not self.vocabulary.has_word(new_word) and is_acceptable(new_word):
                return new_word
            attempts += 1
        warnings.warn('Could not generate unique acceptable word, please check your parameters.')
        return new_word

    def generate_grammar(self):
        if self.morphology not in VALID_MORPHOLOGIES:
            raise ValueError(f'Invalid morphology type: {self.morphology}. Must be one of {VALID_MORPHOLOGIES}.')
        pass

    def mutate(self, sound_change: SoundChange, mutation_rate: float = 0.2) -> Vocabulary:
        new_vocabulary = Vocabulary()
        for item in self.vocabulary:
            word = item['word']
            if self.rng.random() < mutation_rate:
                word = self._generate_unique_word()
            new_word = sound_change.apply(word)
            new_vocabulary.add_item(item['definition'], new_word)
        return new_vocabulary

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'phonemes': self.phonemes,
            'patterns': self.patterns,
            'stress': self.stress,
            'morphology': self.morphology,
            'word_order': self.word_order
        }

    @staticmethod
    def from_json(data: dict) -> 'Language':
        return Language(data['phonemes'], data['patterns'], data['stress'],
                        data['morphology'], data['word_order'], data['id'])
