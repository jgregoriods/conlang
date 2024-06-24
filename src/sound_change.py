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
    # remove double consonants
    for consonant in CONSONANTS:
        fixed_word = re.sub(f'{consonant}{consonant}', consonant, fixed_word)
    return fixed_word


class SoundChange:
    def __init__(self, pipeline: list = list(), tonogenesis: bool = False,
                 random_rules=DEFAULT_RANDOM_RULES):
        self.sound_change_rules = RULES
        self.pipeline = pipeline or self._generate_random_pipeline(random_rules)
        self.tonogenesis = tonogenesis
        print(self.pipeline)

    def _generate_random_pipeline(self, random_rules: int) -> list:
        all_rules = list(self.sound_change_rules.keys()) + [
            'elision_pre',
            'elision_post',
            'final_vowel_deletion',
            'final_consonant_deletion',
            'umlaut',
            'shortening',
            'lengthening',
            'nasalization',
            'vowel_harmony'
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
        
        tone = ''.join([char for char in word if char in ["˩", "˧", "˥"]]).strip()
        word_without_tone = word.replace(tone, '').strip()
        if rule == 'devoicing' and self.tonogenesis:
            for phoneme in split_phonemes(word_without_tone):
                if phoneme in CONSONANTS and 'voiced' in CONSONANTS[phoneme]:
                    tone = "˩" + tone
                    break
            if self.tonogenesis and not tone:
                tone = "˧"
        
        if len(tone) > 2:
            tone = tone[0] + tone[-1]
        
        return ''.join(multiple_replace(word_without_tone, rule_data)) + tone

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
        if rule == 'nasalization':
            return self._apply_nasalization(word)
        if rule == 'vowel_harmony':
            return self._apply_vowel_harmony(word)
        return word

    def _apply_elision_pre(self, word: str) -> str:
        syllables = split_syllables(word)
        if len(syllables) > 1:
            for i in range(1, len(syllables)):
                if "'" in syllables[i]:
                    syllables[i-1] = ''.join([char for char in split_phonemes(syllables[i-1]) if char not in VOWELS])
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
        tone = ''.join([char for char in word if char in ["˩", "˧", "˥"]])
        if self.tonogenesis and not tone:
            tone = "˧"

        word_without_tone = ''.join([char for char in word if char not in ["˩", "˧", "˥"]]).strip()
        phonemes = split_phonemes(word_without_tone)
        for i in range(len(phonemes) - 1, -1, -1):
            if phonemes[i] in VOWELS and i < len(phonemes) - 1 and phonemes[i+1] in CONSONANTS and 'nasal' not in CONSONANTS[phonemes[i+1]]:
                if self.tonogenesis:
                    lost_consonant = phonemes[i+1]
                    if 'plosive' in CONSONANTS[lost_consonant]:
                        tone += "˥"
                    elif 'fricative' in CONSONANTS[lost_consonant]:
                        tone += "˩"
                if len(tone) > 2:
                    tone = tone[0] + tone[-1]
                return ''.join(phonemes[:i+1]) + tone
        if len(tone) > 2:
            tone = tone[0] + tone[-1]
        return word_without_tone + tone

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
            if phonemes[-1] in CONSONANTS and phonemes[-1] not in SEMIVOWELS and 'nasal' not in CONSONANTS[phonemes[-1]]:
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
    
    def _apply_nasalization(self, word: str) -> str:
        syllables = split_syllables(word)
        for i, syllable in enumerate(syllables):
            if syllable[-1] in CONSONANTS and "nasal" in CONSONANTS[syllable[-1]]:
                if syllable[-2] in VOWELS:
                    syllables[i] = syllables[i][:-1] + '̃'
        return ''.join(syllables)
    
    def _apply_vowel_harmony(self, word: str) -> str:
        front = 'iyeɛøæ'
        harmony = {
            'front': {
                'a': 'ɛ',
                'o': 'ø',
                'u': 'y',
                'ɒ': 'œ',
                'ɔ': 'ø',
                'ɑ': 'æ',
                'ʌ': 'œ',
                'ɜ': 'ɛ',
                'ə': 'ɛ',
                'ɐ': 'ɛ'
            },
            'not_front': {
                'i': 'ɯ',
                'y': 'ʉ',
                'e': 'ɤ',
                'ɛ': 'œ',
                'ø': 'ɤ',
            }
        }
        phonemes = split_phonemes(word)
        rule = None
        for i, phoneme in enumerate(phonemes):
            if phoneme in VOWELS:
                if rule is None:
                    first_vowel = phoneme[0]
                    if first_vowel in front:
                        rule = 'front'
                    else:
                        rule = 'not_front'
                else:
                    if phoneme[0] in harmony[rule]:
                        phonemes[i] = phonemes[i].replace(phoneme[0], harmony[rule][phoneme[0]])

        return ''.join(phonemes)
    
    def apply(self, word: str) -> str:
        for rule in self.pipeline:
            word = common_fixes(self.apply_sound_change(rule, word))
        return word
