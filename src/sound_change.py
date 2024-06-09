import re

from numpy import random
from .vocabulary import Vocabulary
from .utils import split_syllables, split_phonemes
from .phonemes import VOWELS


def multiple_replace(word, rules):
    replace_dict, condition = rules
    syllables = split_syllables(word)
    syllable_phonemes = [split_phonemes(syllable) for syllable in syllables]

    res = []

    for i, syllable in enumerate(syllable_phonemes):
        if condition == 'stressed':
            if "'" in syllable:
                for phoneme in syllable:
                    if phoneme in replace_dict:
                        res.append(replace_dict[phoneme])
                    else:
                        res.append(phoneme)
            else:
                res.extend(syllable)
        elif condition == 'unstressed':
            if "'" not in syllable:
                for phoneme in syllable:
                    if phoneme in replace_dict:
                        res.append(replace_dict[phoneme])
                    else:
                        res.append(phoneme)
            else:
                res.extend(syllable)
        elif 'next' in condition:
            next_phonemes = condition['next']
            for j in range(len(syllable)):
                if j < len(syllable) - 1 and syllable[j+1] in next_phonemes:
                    if syllable[j] in replace_dict:
                        res.append(replace_dict[syllable[j]])
                    else:
                        res.append(syllable[j])
                else:
                    res.append(syllable[j])
        else:
            for phoneme in syllable:
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
        rule, condition = rules
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
            if len(syllables) > 1:
                if "'" not in syllables[-1]:
                    regex = re.compile('|'.join(list(VOWELS) + [':']))
                    syllables[-1] = re.sub(regex, '', syllables[-1])
            return ''.join(syllables)

        if rule == 'FINAL_CONSONANT_DELETION':
            for i in range(len(word) - 1, -1, -1):
                if word[i] in list(VOWELS) + [':']:
                    return word[:i+1]

        return ''.join(multiple_replace(word, rules))

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

