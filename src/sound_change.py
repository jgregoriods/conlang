import re
from numpy import random
from .utils import split_phonemes, split_syllables, multiple_replace
from .phonemes import CONSONANTS, SEMIVOWELS, VOWELS
from .rules import RULES


DEFAULT_RANDOM_RULES = 3


def common_fixes(word: str) -> str:
    syllables = split_syllables(word)
    for i, syllable in enumerate(syllables):
        if "'" in syllable and syllable[0] != "'":
            syllables[i] = "'" + syllable.replace("'", "")
    fixed_word = ''.join(syllables)
    return fixed_word


class SoundChange:
    def __init__(self, pipeline: list = list(), random_rules=DEFAULT_RANDOM_RULES):
        self.sound_change_rules = RULES
        self.pipeline = pipeline or self._generate_random_pipeline(random_rules)
        print(self.pipeline)

    def _generate_random_pipeline(self, random_rules: int) -> list:
        all_rules = list(self.sound_change_rules.keys()) + [
            'elision_pre',
            'elision_post',
            'final_vowel_deletion',
            'final_consonant_deletion',
            'umlaut',
            'shortening',
            'lengthening'
        ]
        n_rules = min(random_rules, len(all_rules))
        return random.choice(all_rules, n_rules, replace=False).tolist()

    def apply_sound_change(self, rule: str, word: str) -> str:
        if rule in self.sound_change_rules:
            return self._apply_rule_from_dict(rule, word)
        return self._apply_custom_rule(rule, word)

    def _apply_rule_from_dict(self, rule: str, word: str) -> str:
            rule_data = self.sound_change_rules[rule]
            if 'condition' in rule_data:
                if rule_data['condition'] == 'stressed':
                    return self._apply_stressed_rule(rule_data, word)
                elif rule_data['condition'] == 'unstressed':
                    return self._apply_unstressed_rule(rule_data, word)
            return ''.join(multiple_replace(word, rule_data))

    def _apply_stressed_rule(self, rule_data: dict, word: str) -> str:
        syllables = split_syllables(word)
        for i, syllable in enumerate(syllables):
            if "'" in syllable:
                syllables[i] = multiple_replace(syllable, rule_data)
                break
        return ''.join(syllables)

    def _apply_unstressed_rule(self, rule_data: dict, word: str) -> str:
        syllables = split_syllables(word)
        for i, syllable in enumerate(syllables):
            if "'" not in syllable:
                syllables[i] = multiple_replace(syllable, rule_data)
                break
        return ''.join(syllables)

    def _apply_custom_rule(self, rule: str, word: str) -> str:
        if rule == 'elision_pre':
            return self._apply_elision_pre(word)
        if rule == 'elision_post':
            return self._apply_elision_post(word)
        if rule == 'final_vowel_deletion':
            return self._apply_final_vowel_deletion(word)
        if rule == 'final_consonant_deletion':
            return self._apply_final_consonant_deletion(word)
        if rule == 'umlaut':
            return self._apply_umlaut(word)
        if rule == 'shortening':
            return self._apply_shortening(word)
        if rule == 'lengthening':
            return self._apply_lengthening(word)
        return word

    def _apply_elision_pre(self, word: str) -> str:
        syllables = split_syllables(word)
        if len(syllables) > 1:
            for i in range(1, len(syllables)):
                if "'" in syllables[i]:
                    regex = re.compile('|'.join(list(VOWELS) + SEMIVOWELS + [':']))
                    syllables[i-1] = re.sub(regex, '', syllables[i-1])
                    break
        return ''.join(syllables)

    def _apply_elision_post(self, word: str) -> str:
        syllables = split_syllables(word)
        if len(syllables) > 1:
            for i in range(len(syllables) - 1):
                if "'" in syllables[i]:
                    regex = re.compile('|'.join(list(VOWELS) + SEMIVOWELS + [':']))
                    syllables[i+1] = re.sub(regex, '', syllables[i+1])
                    break
        return ''.join(syllables)

    def _apply_final_vowel_deletion(self, word: str) -> str:
        syllables = split_syllables(word)
        if len(syllables) > 1 and "'" not in syllables[-1]:
            for i in range(len(syllables[-1]) - 1, -1, -1):
                if syllables[-1][i] not in list(VOWELS) + SEMIVOWELS + [':']:
                    syllables[-1] = syllables[-1][:i+1]
                    break
        return ''.join(syllables)

    def _apply_final_consonant_deletion(self, word: str) -> str:
        for i in range(len(word) - 1, -1, -1):
            if word[i] in list(VOWELS) + SEMIVOWELS + [':']:
                return word[:i+1]
        return word

    def _apply_umlaut(self, word: str) -> str:
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

    def _apply_shortening(self, word: str) -> str:
        syllables = split_syllables(word)
        for i, syllable in enumerate(syllables):
            if "'" not in syllable:
                syllables[i] = syllable.replace(":", '')
        return ''.join(syllables)

    def _apply_lengthening(self, word: str) -> str:
        syllables = split_syllables(word)
        for i, syllable in enumerate(syllables):
            phonemes = split_phonemes(syllable)
            if phonemes[-1] in CONSONANTS:
                vowel_idx = [phonemes.index(p) for p in phonemes if p in VOWELS][-1]
                phonemes[vowel_idx] += ':'
                syllables[i] = ''.join(phonemes[:-1])
        for i in range(1, len(syllables)):
            if syllables[i][0] in VOWELS:
                if syllables[i-1] and syllables[i-1][-1] == syllables[i][0]:
                    syllables[i] = syllables[i][1:]
                    syllables[i-1] += ":"
            elif syllables[i][0] == "'" and syllables[i][1] in VOWELS:
                if syllables[i-1] and (syllables[i-1][-1] == syllables[i][1]):
                    syllables[i] = syllables[i][2:]
                    syllables[i-1] += ":"
                    syllables[i-1] = "'" + syllables[i-1]
        return ''.join(syllables)

    def apply(self, word: str) -> str:
        for rule in self.pipeline:
            word = common_fixes(self.apply_sound_change(rule, word))
        return word
