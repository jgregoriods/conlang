import numpy as np
import warnings
import json
import uuid

from .sound_change import SoundChange
from .vocabulary import Vocabulary, SWADESH
from .utils import split_phonemes, split_syllables, get_prob_dist
from .phonemes import VOWELS, CONSONANTS


VALID_MORPHOLOGIES = {'agglutinative', 'fusional', 'isolating', 'polysynthetic'}
VALID_POS = {'S', 'O', 'V'}
MAX_ATTEMPTS = 100


def parse_word(word: str):
    phonemes = split_phonemes(word)
    # split consonants and vowels
    start = 0
    res = []
    current_type = None
    for i, char in enumerate(phonemes):
        if current_type is None:
            if char in VOWELS:
                current_type = 'V'
            elif char in CONSONANTS:
                current_type = 'C'
        elif char in VOWELS and current_type == 'C':
            res.append(phonemes[start:i])
            start = i
            current_type = 'V'
        elif char in CONSONANTS and current_type == 'V':
            res.append(phonemes[start:i])
            start = i
            current_type = 'C'
    res.append(phonemes[start:])
    return res


def parse_vocabulary(vocabulary):
    stress = set()
    phonemes = {'C1': [], 'C2': [], 'C3': [],
                'V1': [], 'V2': [], 'V3': []}
    patterns = set()
    tones = set()
    for item in vocabulary:
        word = item['word']
        tone = ''.join([char for char in word if char in ["˩", "˧", "˥"]])
        tones.add(tone)
        syllables = split_syllables(word)
        for i, syllable in enumerate(syllables):
            if syllable.startswith("ˈ"):
                stress.add(i - len(syllables))
        no_stress = word.replace("ˈ", "").replace("˩", "").replace("˧", "").replace("˥", "")
        phoneme_groups = parse_word(no_stress)
        pattern = ''
        if len(phoneme_groups) > 1:
            if phoneme_groups[0][0] in VOWELS:
                phonemes['V1'].append(''.join(phoneme_groups[0]))
                pattern += 'V1 '
            elif phoneme_groups[0][0] in CONSONANTS:
                phonemes['C1'].append(''.join(phoneme_groups[0]))
                pattern += 'C1 '

            for group in phoneme_groups[1:-1]:
                if group[0] in VOWELS:
                    phonemes['V2'].append(''.join(group))
                    pattern += 'V2 '
                elif group[0] in CONSONANTS:
                    phonemes['C2'].append(''.join(group))
                    pattern += 'C2 '
    
            if phoneme_groups[-1][0] in VOWELS:
                phonemes['V3'].append(''.join(phoneme_groups[-1]))
                pattern += 'V3'
            elif phoneme_groups[-1][0] in CONSONANTS:
                phonemes['C3'].append(''.join(phoneme_groups[-1]))
                pattern += 'C3'

            patterns.add(pattern)
        else:
            if phoneme_groups[0][0] in VOWELS:
                phonemes['V1'].append(''.join(phoneme_groups[0]))
                patterns.add('V1')

    phonemes = {k: v for k, v in phonemes.items() if v}
    phonemes = {k: sorted(list(set(v)), key=lambda x: v.count(x), reverse=True) for k, v in phonemes.items()}
    return {'phonemes': phonemes, 'stress': list(stress), 'patterns': list(patterns), 'tones': list(tones)}


def is_acceptable(word: str, ratio: float = 0.67) -> bool:
    word = [phoneme for phoneme in word if phoneme != "ˈ"]
    # for short words we are more lenient
    if len(word) < 3:
        return True

    # avoid too many long vowels or aspirations
    for char in ["ː", "ʰ"]:
        if word.count(char) > 1:
            return False

    # avoid ending in aspiration
    if word[-1] in ['ʰ']:
        return False

    # avoid repetitive phonemes
    if len(set(word)) / len(word) < ratio:
        return False

    # avoid the same consonant in close proximity
    for i in range(len(word) - 2):
        if word[i] in CONSONANTS:
            if word[i] == word[i + 1] or word[i] == word[i + 2]:
                return False
    if word[-2] in CONSONANTS and word[-2] == word[-1]:
        return False

    return True


class Language:
    def __init__(self, phonemes: dict, patterns: list, stress: list,
                 tones: list = [],
                 morphology: str = 'fusional', word_order: str = 'SVO',
                 id: str = ''):
        self.phonemes = phonemes
        self.patterns = patterns
        self.stress = stress
        self.tones = tones
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
        syllables[stressed_syllable] = "ˈ" + syllables[stressed_syllable]

        word = ''.join(syllables)

        if self.tones:
            tone = self.rng.choice(self.tones)
            word += tone
        
        return word

    def generate_vocabulary(self, adjust_length: bool = True):
        self.vocabulary = Vocabulary(self.id)
        for item in SWADESH:
            # if adjust_length is True, the most frequent words will be shorter
            short_patterns = sorted(self.patterns, key=lambda x: len(x.split()))[:2]
            sel_patterns = short_patterns if adjust_length and item[2] == 1 else self.patterns
            new_word = self._generate_unique_word(sel_patterns)
            self.vocabulary.add_item(item[0], new_word)
        unique_words = set([item['word'] for item in self.vocabulary])
        if len(unique_words) < len(self.vocabulary) * 0.67:
            warnings.warn('There are too many homonyms. Consider adding tones.')

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

    def mutate(self, sound_change: SoundChange, mutation_rate: float = 0.1) -> Vocabulary:
        new_vocabulary = Vocabulary()
        for item in self.vocabulary:
            word = item['word']
            if self.rng.random() < mutation_rate:
                word = self._generate_unique_word()
            new_word = sound_change.apply(word)
            new_vocabulary.add_item(item['definition'], new_word)
        unique_words = set([item['word'] for item in new_vocabulary])
        if len(unique_words) < len(new_vocabulary) * 0.67:
            warnings.warn('There are too many homonyms. Consider adding tones.')
        return new_vocabulary

    def generate_family(self, num_children: int, sound_changes: list = list()) -> list:
        if sound_changes and len(sound_changes) != num_children:
            raise ValueError('Number of sound change pipelines must match number of children.')
        if not sound_changes:
            sound_changes = [SoundChange() for _ in range(num_children)]
        family = []
        for _ in range(num_children):
            for change in sound_changes:
                new_vocabulary = self.mutate(change)
                new_language = Language.from_vocabulary(new_vocabulary)
                family.append(new_language)
        return family

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
        return Language(phonemes=data['phonemes'], patterns=data['patterns'],
                        stress=data['stress'], morphology=data['morphology'],
                        word_order=data['word_order'], id=data['id'])

    @staticmethod
    def from_vocabulary(vocabulary: Vocabulary) -> 'Language':
        parsed_vocabulary = parse_vocabulary(vocabulary)
        new_language = Language(parsed_vocabulary['phonemes'], parsed_vocabulary['patterns'], parsed_vocabulary['stress'])
        new_language.vocabulary = vocabulary
        return new_language
