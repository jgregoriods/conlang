import re

from numpy import random
from .vocabulary import Vocabulary
from .utils import split_syllables, multiple_replace
from .phonemes import SEMIVOWELS, VOWELS



class SoundChange:
    def __init__(self, pipeline=list(), random_rules=3):
        self.sound_change_rules = {
            'opening_1': {
                'rules' : {
                    'p': 'ɸ',
                    't': 'θ',
                    'k': 'x',
                    'ts': 's',
                    'ɸ': 'h',
                    'θ': 'h',
                    'x': 'h',
                    's': 'h',
                    'h': ''
                    },
                },
            'opening_2': {
                'rules' : {
                    'p': 'f',
                    't': 's',
                    'k': 'x',
                    'f': 'h',
                    's': 'h',
                    'x': 'h',
                    'h': ''
                    },
                },
            'sonorization_1': {
                'rules' : {
                    'p': 'b',
                    't': 'd',
                    'k': 'g',
                    'ts': 'dz',
                    'b': 'β',
                    'd': 'ð',
                    'g': 'ɣ',
                    'β': 'w',
                    'ð': 'ɹ',
                    'ɣ': 'j',
                    'w': '',
                    'ɹ': '',
                    'j': ''
                    },
                },
            'sonorization_2': {
                'rules' : {
                    'p': 'b',
                    't': 'd',
                    'k': 'g',
                    'b': 'v',
                    'd': 'z',
                    'g': 'ɣ',
                    'v': 'w',
                    'z': 'ɹ',
                    'ɣ': 'j',
                    'w': '',
                    'ɹ': '',
                    'j': ''
                    },
                },
            'grimms_law': {
                'rules' : {
                    'p': 'f',
                    't': 'θ',
                    'k': 'x',
                    'b': 'p',
                    'd': 't',
                    'g': 'k',
                    'bʰ': 'b',
                    'dʰ': 'd',
                    'gʰ': 'g'
                    },
                },
            'great_vowel_shift': {
                'rules' : {
                    'i:': 'aɪ',
                    'e:': 'i:',
                    'ɛ:': 'eɪ',
                    'a:': 'eɪ',
                    'u:': 'aʊ',
                    'o:': 'u:',
                    'ɔ:': 'oʊ'
                    },
                },
            'palatalization_1': {
                'rules' : {
                    'k I': 'tʃ I',
                    'g I': 'dʒ I',
                    'x I': 'ç I',
                    'ɣ I': 'ʝ I',
                    'j I': 'ʝ I',
                    },
                'wildcards': {
                    'I': ['i', 'e', 'e:', 'i:', 'ɛ', 'ɪ', 'ɛ:', 'j', 'ɪ:']
                    }
                },
            'palatalization_2': {
                'rules' : {
                    't I': 'tʃ I',
                    'd I': 'dʒ I',
                    's I': 'ʃ I',
                    'z I': 'ʒ I',
                    'n I': 'ɲ I',
                    'l I': 'ʎ I'
                    },
                'wildcards': {
                    'I': ['i', 'e', 'e:', 'i:', 'ɛ', 'ɪ', 'ɛ:', 'j', 'ɪ:']
                    }
                },
            'canaanite_shift': {
                'rules' : {
                    'a:': 'o:',
                    },
                },
            'yiddish_breaking': {
                'rules' : {
                    'ɛ:': 'ɛj',
                    'o:': 'ɔj',
                    'ø:': 'ɛj',
                    'i:': 'aj',
                    'y:': 'aj',
                    'u:': 'ɔj'
                    },
                'condition': 'stressed'
                },
            'romance_breaking': {
                'rules' : {
                    'e': 'je',
                    'o': 'wo',
                    'ɛ': 'jɛ',
                    'ɔ': 'wɔ'
                    },
                'condition': 'stressed'
                },
        }

        self.pipeline = pipeline
        if not self.pipeline:
            all_rules = list(self.sound_change_rules.keys())
            all_rules += [
                'elision_pre',
                'elision_post',
                'final_vowel_deletion',
                'final_consonant_deletion'
            ]
            n_rules = min(random_rules, len(all_rules))
            self.pipeline = random.choice(all_rules, n_rules, replace=False)

        print(self.pipeline)

    def apply_sound_change(self, rule, word):

        if rule == 'elision_pre':
            syllables = split_syllables(word)
            if len(syllables) > 1:
                for i in range(1, len(syllables)):
                    if "'" in syllables[i]:
                        regex = re.compile('|'.join(list(VOWELS) + SEMIVOWELS + [':']))
                        syllables[i-1] = re.sub(regex, '', syllables[i-1])
                        break
            return ''.join(syllables)

        if rule == 'elision_post':
            syllables = split_syllables(word)
            if len(syllables) > 1:
                for i in range(len(syllables) - 1):
                    if "'" in syllables[i]:
                        regex = re.compile('|'.join(list(VOWELS) + SEMIVOWELS + [':']))
                        syllables[i+1] = re.sub(regex, '', syllables[i+1])
                        break
            return ''.join(syllables)

        if rule == 'final_vowel_deletion':
            syllables = split_syllables(word)
            if len(syllables) > 1 and "'" not in syllables[-1]:
                for i in range(len(syllables[-1]) - 1, -1, -1):
                    if syllables[-1][i] not in list(VOWELS) + SEMIVOWELS + [':']:
                        syllables[-1] = syllables[-1][:i+1]
                        break
            return ''.join(syllables)

        if rule == 'final_consonant_deletion':
            for i in range(len(word) - 1, -1, -1):
                if word[i] in list(VOWELS) + SEMIVOWELS + [':']:
                    return word[:i+1]

        if rule == 'umlaut':
            umlaut = {
                'rules': {
                    'a': 'ɛ',
                    'u': 'y',
                    'o': 'ø',
                    'a:': 'ɛ:',
                    'u:': 'y:',
                    'o:': 'ø:'
                }
            }
            syllables = split_syllables(word)
            for i, syllable in enumerate(syllables[:-1]):
                if set(syllables[i+1]) & set('iey'):
                    syllables[i] = multiple_replace(syllable, umlaut)
            return ''.join(syllables)


        if rule in self.sound_change_rules:
            rule_data = self.sound_change_rules[rule]
            if 'condition' in rule_data:
                if rule_data['condition'] == 'stressed':
                    syllables = split_syllables(word)
                    for i, syllable in enumerate(syllables):
                        if "'" in syllable:
                            syllables[i] = multiple_replace(syllable, rule_data)
                            break
                    return ''.join(syllables)
                elif rule_data['condition'] == 'unstressed':
                    syllables = split_syllables(word)
                    for i, syllable in enumerate(syllables):
                        if "'" not in syllable:
                            syllables[i] = multiple_replace(syllable, rule_data)
                            break
                    return ''.join(syllables)

            return ''.join(multiple_replace(word, rule_data))

        return word

    def apply(self, word):
        for rule in self.pipeline:
            word = self.apply_sound_change(rule, word)
        return word
