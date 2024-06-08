import re

from numpy import random
from .vocabulary import Vocabulary
from .utils import split_syllables, split_phonemes
from .phonemes import VOWELS


# It is true that we could use regex for this,
# but this function will make things easier when
# we start adding more complex rules.
def multiple_replace(phonemes, replace_dict):
    res = []
    for phoneme in phonemes:
        if phoneme in replace_dict:
            res.append(replace_dict[phoneme])
        else:
            res.append(phoneme)
    return res


class SoundChange:
    def __init__(self, pipeline, mutation_rate):
        self.pipeline = pipeline
        self.mutation_rate = mutation_rate

    def apply(self, rules, word):
        if rules == 'ELISION_PRE':
            syllables = split_syllables(word)
            if len(syllables) > 1:
                for i in range(1, len(syllables)):
                    if "'" in syllables[i]:
                        regex = re.compile('|'.join(list(VOWELS) + [':']))
                        syllables[i-1] = re.sub(regex, '', syllables[i-1])
                        break
            return ''.join(syllables)

        if rules == 'ELISION_POST':
            syllables = split_syllables(word)
            if len(syllables) > 1:
                for i in range(len(syllables) - 1):
                    if "'" in syllables[i]:
                        regex = re.compile('|'.join(list(VOWELS) + [':']))
                        syllables[i+1] = re.sub(regex, '', syllables[i+1])
                        break
            return ''.join(syllables)

        # regex = re.compile('|'.join(map(re.escape, rules)))
        # return regex.sub(lambda match: rules[match.group(0)], word)

        phonemes = split_phonemes(word)
        return ''.join(multiple_replace(phonemes, rules))

    def evolve(self, language):
        new_vocabulary = Vocabulary()
        for item in language.vocabulary.items:
            definition, new_word = item['definition'], item['word']
            if random.random() < self.mutation_rate:
                new_word = language.generate_word()
            for rule in self.pipeline:
                new_word = self.apply(rule, new_word)
            new_vocabulary.add_item(definition, new_word)
        return new_vocabulary

