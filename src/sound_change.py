import re

from numpy import random
from .vocabulary import Vocabulary
from .utils import split_syllables, split_phonemes
from .phonemes import VOWELS
from .rules import RULES


def multiple_replace(word, repl_dict):
    phonemes = split_phonemes(word)

    res = []

    for i, phoneme in enumerate(phonemes):
        if phoneme in repl_dict:
            res.append(repl_dict[phoneme])
        else:
            res.append(phoneme)
    return res


class SoundChange:
    def __init__(self, pipeline, mutation_rate):
        self.pipeline = pipeline
        self.mutation_rate = mutation_rate

    def apply(self, rule, word):
        if rule in RULES:
            repl_dict = RULES[rule]['rules']
            return ''.join(multiple_replace(word, repl_dict))

        if rule == 'ELISION_PRE':
            syllables = split_syllables(word)
            if len(syllables) > 1:
                for i in range(1, len(syllables)):
                    if "'" in syllables[i]:
                        regex = re.compile('|'.join(list(VOWELS) + [':']))
                        syllables[i-1] = re.sub(regex, '', syllables[i-1])
                        break
            return ''.join(syllables)

        if rule == 'ELISION_POST':
            syllables = split_syllables(word)
            if len(syllables) > 1:
                for i in range(len(syllables) - 1):
                    if "'" in syllables[i]:
                        regex = re.compile('|'.join(list(VOWELS) + [':']))
                        syllables[i+1] = re.sub(regex, '', syllables[i+1])
                        break
            return ''.join(syllables)

        if rule == 'FINAL_VOWEL_DELETION':
            syllables = split_syllables(word)
            if len(syllables) > 1 and "'" not in syllables[-1]:
                for i in range(len(syllables[-1]), -1, -1):
                    if syllables[-1][i] not in list(VOWELS) + [':']:
                        syllables[-1] = syllables[-1][:i+1]
                        break
            return ''.join(syllables)

        if rule == 'FINAL_CONSONANT_DELETION':
            for i in range(len(word) - 1, -1, -1):
                if word[i] in list(VOWELS) + [':']:
                    return word[:i+1]


    def evolve(self, language):
        new_vocabulary = Vocabulary()
        for item in language.vocabulary.items:
            definition, new_word = item['definition'], item['word']
            if random.random() < self.mutation_rate:
                new_word = language.generate_word()
            for rules in self.pipeline:
                new_word = self.apply(rules, new_word)
            new_vocabulary.add_item(definition, new_word)
        return new_vocabulary

