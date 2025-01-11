import numpy as np

from .swadesh import SWADESH
from .vocabulary import Vocabulary
from .language_config import LanguageConfig
from .utils import split_syllables, is_acceptable


MAX_ATTEMPTS = 10


class Language:
    def __init__(self, name: str, config: LanguageConfig, vocabulary=None):
        self.name = name
        self.config = config
        self.vocabulary = vocabulary

    def generate_word(self, rank: int = -1) -> str:
        pattern = np.random.choice(
            self.config.patterns[:2] if 0 <= rank < 25 else self.config.patterns)

        res = ''
        for k in pattern:
            res += np.random.choice(self.config.phonemes[k])

        syllables = split_syllables(res)

        stressed = max(np.random.choice(self.config.stress), -len(syllables))
        syllables[stressed] = "ˈ" + syllables[stressed]

        word = ''.join(syllables)

        return word

    def generate_vocabulary(self, glosses: list = None):
        vocabulary = Vocabulary()
        glosses = glosses or SWADESH
        # patterns = sorted(self.config.patterns, key=len)
        # phonemes = process_phonemes(self.config.phonemes)
        for gloss in glosses:
            idx = SWADESH.index(gloss) if gloss in SWADESH else -1
            attempts = 0
            while attempts < MAX_ATTEMPTS:
                word = self.generate_word(rank=idx)
                if is_acceptable(word) and not vocabulary.has_word(word):
                    break
                attempts += 1
            vocabulary.add_item(word, gloss)
        self.vocabulary = vocabulary
