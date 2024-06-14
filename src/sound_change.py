import re

from numpy import random
from .vocabulary import Vocabulary
from .utils import split_syllables, split_phonemes
from .phonemes import VOWELS
from .rules import RULES


def multiple_replace(word, rule):
    repl_dict = rule['rules']
    if 'wildcards' in rule:
        new_repl_dict = {}
        for k, v in repl_dict.items():
            for wildcard in rule['wildcards']:
                if wildcard in k:
                    for i in rule['wildcards'][wildcard]:
                        new_key = k.replace(wildcard, i)
                        new_value = v.replace(wildcard, i)
                        new_repl_dict[new_key] = new_value
        repl_dict.update(new_repl_dict)
    phonemes = f" {' '.join(split_phonemes(word))} "
    d = {f' {k} ': f' {v} ' for k, v in repl_dict.items()}
    regex = re.compile('|'.join(map(re.escape, d.keys())))
    new_phonemes = re.sub(regex, lambda match: d[match.group(0)], phonemes)
    return new_phonemes.replace(' ', '')


class SoundChange:
    def __init__(self, pipeline, mutation_rate):
        self.pipeline = pipeline
        self.mutation_rate = mutation_rate

    def apply(self, rule, word):

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

        return ''.join(multiple_replace(word, rule))



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

