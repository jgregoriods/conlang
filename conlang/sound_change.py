from itertools import product
from pathlib import Path
import re
from typing import List, Dict, Tuple, Optional
import numpy as np
from .phonemes import VOWEL_SET, CONSONANT_SET, PHONEME_FEATURE_DICT, FEATURE_MAPPING, BOOLEAN_PROPS
from .rules import RULES
from .utils import parse_phonemes, get_matching_phoneme
from .vocabulary import Vocabulary
from .word import Word


class SoundChange:
    """
    A class to handle phonological sound changes using defined rules.

    Attributes:
        rules (Dict[Tuple[str], List[Tuple[str]]]): A dictionary mapping phonemes or phoneme
                                                    sequences to lists of tuples, where each tuple
                                                    contains the new phoneme(s) and the environment.
        wildcards (Optional[Dict[str, List[str]]]): A dictionary mapping wildcard symbols to lists
                                                    of phonemes.
    """

    def __init__(self, rules: Dict[Tuple[str], List[Tuple[str]]],
                 wildcards: Optional[Dict[str, List[str]]] = None):
        """
        Initializes a SoundChange instance.

        Args:
            rules (Dict[Tuple[str], List[Tuple[str]]]): A dictionary of sound change rules.
            wildcards (Optional[Dict[str, List[str]]]): A dictionary of wildcard mappings.
                                                        Defaults to None.
        """
        self.rules = rules
        self.wildcards = wildcards
        self.feature_based_rules = {k: v for k, v in rules.items() if '[' in k[0]}
        self.phoneme_based_rules = {k: v for k, v in rules.items() if '[' not in k[0]}

    def apply_to_word(self, word: Word) -> Word:
        """
        Apply sound changes to a single word based on defined rules.

        Args:
            word (Word): The input word.

        Returns:
            Word: The transformed word.
        """
        stress_start, stress_end = word.stress_bounds
        phonemes = word.phonemes
        result = []

        def matches_sequence(start_idx: int, sequence: Tuple[str]) -> bool:
            """
            Check if a sequence of phonemes matches the input phonemes starting at the given index.

            Args:
                start_idx (int): The starting index in the phonemes list.
                sequence (Tuple[str]): The sequence of phonemes to match.

            Returns:
                bool: True if the sequence matches, False otherwise.
            """
            if start_idx + len(sequence) > len(phonemes):
                return False
            for i, phoneme in enumerate(sequence):
                if phoneme in 'CV' or phoneme in self.wildcards:
                    if not self._matches_phoneme(phonemes[start_idx + i], phoneme):
                        return False
                elif phonemes[start_idx + i] != phoneme:
                    return False
            return True

        def matches_environment(start_idx: int, end_idx: int, environment: str) -> bool:
            """
            Check if the phoneme at the given index matches the environment.

            Args:
                start_idx (int): The starting index of the phoneme sequence.
                end_idx (int): The ending index of the phoneme sequence.
                environment (str): The environment string (e.g., "#_", "_#", "V_V").

            Returns:
                bool: True if the environment matches, False otherwise.
            """
            if not environment:
                return True

            if environment == "#_":
                return start_idx == 0
            if environment == "_#":
                return end_idx == len(phonemes) - 1

            prv, nxt = environment.split(
                '_') if '_' in environment else (None, None)

            if prv:
                if prv == '#':
                    if start_idx != 0:
                        return False

                else:
                    prev_idx = start_idx - 1
                    if prev_idx < 0 or not self._matches_phoneme(phonemes[prev_idx], prv):
                        return False

            if nxt:
                if nxt == '#':
                    if end_idx != len(phonemes) - 1:
                        return False

                else:
                    next_idx = end_idx + 1
                    if next_idx >= len(phonemes) or not self._matches_phoneme(phonemes[next_idx], nxt):
                        return False

            return True

        i = 0
        while i < len(phonemes):
            matched = False

            # Check for the longest matching sequence first
            for sequence_length in range(max(len(k) for k in self.phoneme_based_rules.keys()), 0, -1):
                if i + sequence_length > len(phonemes):
                    continue

                sequence = tuple(phonemes[i:i + sequence_length])
                possible_keys = [sequence]

                # Add wildcard-based keys (e.g., ('V', 't') for ('a', 't'))
                combinations = []
                for key in possible_keys:
                    replacement_options = []
                    for phoneme in key:
                        options = []
                        if phoneme in VOWEL_SET:
                            options.append('V')
                        if phoneme in CONSONANT_SET:
                            options.append('C')
                        for wildcard, wildcard_phonemes in self.wildcards.items():
                            if phoneme in wildcard_phonemes:
                                options.append(wildcard)
                        options.append(phoneme)
                        replacement_options.append(options)
                    combinations.extend([tuple(repl) for repl in set(
                        list(product(*replacement_options)))])
                possible_keys.extend(combinations)

                for key in possible_keys:
                    if key in self.rules:
                        for after, environment in self.rules[key]:
                            # Handle stress-specific environments
                            if ('[+stress]' in environment and not stress_start <= i < stress_end) or \
                                    ('[-stress]' in environment and stress_start <= i < stress_end):
                                continue

                            environment = environment.replace(
                                '[+stress]', '').replace('[-stress]', '').strip()

                            if matches_sequence(i, key) and matches_environment(i, i + sequence_length - 1, environment):
                                if 'V' in after:
                                    original_vowels = [
                                        p for p in phonemes[i:i + sequence_length] if p in VOWEL_SET]
                                    for vowel in original_vowels:
                                        after = after.replace('V', vowel, 1)
                                    after = after.replace('ː̃', '̃ː')
                                result.append(after)
                                i += sequence_length
                                matched = True
                                break

                    if matched:
                        break
                if matched:
                    break
            
            for feature_key in self.feature_based_rules.keys():
                for after, environment in self.feature_based_rules[feature_key]:
                    if ('[+stress]' in environment and not stress_start <= i < stress_end) or \
                            ('[-stress]' in environment and stress_start <= i < stress_end):
                        continue

                    environment = environment.replace(
                        '[+stress]', '').replace('[-stress]', '').strip()

                    if matches_sequence(i, feature_key) and matches_environment(i, i, environment):
                        if "[" in after:
                            features = self._prop_from_condition(after)
                            prop, (value, positive) = list(features.items())[0]
                            if prop in BOOLEAN_PROPS or positive:
                                feature_dict = {prop: value}
                            else:
                                feature_dict = {}
                            after = get_matching_phoneme(phonemes[i], feature_dict)
                        result.append(after)
                        i += 1
                        matched = True
                        break
                
                if matched:
                    break

            if not matched:
                result.append(phonemes[i])
                i += 1

        # Remove null phonemes (e.g., ∅ or 0)
        mutated_word = Word(re.sub('[∅0]', '', ''.join(result)))
        mutated_word.set_stress(word.stress)
        return mutated_word

    def apply_to_vocabulary(self, vocabulary: Vocabulary) -> Vocabulary:
        """
        Apply sound changes to an entire vocabulary.

        Args:
            vocabulary (Vocabulary): The input vocabulary.

        Returns:
            Vocabulary: A new vocabulary with mutated words.
        """
        if not self.rules:
            raise ValueError('No rules defined for sound change')
        mutated_vocabulary = Vocabulary()
        for word, gloss in vocabulary:
            mutated_word = self.apply_to_word(word)
            mutated_vocabulary.add_item(mutated_word, gloss)
        return mutated_vocabulary

    @staticmethod
    def from_str(string: str) -> 'SoundChange':
        """
        Create a SoundChange instance from a string of rules.

        Args:
            string (str): The string containing rules and wildcards.

        Returns:
            SoundChange: A new instance with parsed rules and wildcards.
        """
        rules = {}
        wildcards = {}

        for line in string.splitlines():
            line = line.strip()
            if not line or line.startswith('['):
                continue
            if '>' in line:
                before, after = map(str.strip, line.split('>'))
                before = tuple([before]) if "[" in before else tuple(parse_phonemes(before))
                environment = ''
                if '/' in after:
                    after, environment = map(str.strip, after.split('/'))
                rules.setdefault(before, []).append((after, environment))
            elif ':' in line:
                wildcard, phonemes = map(str.strip, line.split(':'))
                wildcards[wildcard] = phonemes.split()

        return SoundChange(rules, wildcards)

    @staticmethod
    def from_txt(file_path: str) -> 'SoundChange':
        """
        Create a SoundChange instance from a text file of rules.

        Args:
            file_path (str): The path to the file.

        Returns:
            SoundChange: A new instance with parsed rules and wildcards.
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f'File not found: {file_path}')
        with path.open('r', encoding='utf-8') as f:
            return SoundChange.from_str(f.read())

    @staticmethod
    def random() -> 'SoundChange':
        """
        Generate a random SoundChange instance from predefined rules.

        Returns:
            SoundChange: A new instance with random rules and wildcards.
        """
        selected_rules = np.random.choice(list(RULES.keys()))
        return SoundChange(RULES[selected_rules]['rules'], RULES[selected_rules]['wildcards'])

    @staticmethod
    def load_preset(name: str) -> 'SoundChange':
        """
        Load a SoundChange instance from a predefined preset.

        Args:
            name (str): The name of the preset.

        Returns:
            SoundChange: A new instance with rules and wildcards from the preset.
        """
        if name not in RULES:
            raise ValueError(f'Preset not found: {name}')
        return SoundChange(RULES[name]['rules'], RULES[name]['wildcards'])

    def _prop_from_condition(self, condition: str) -> Dict[str, Tuple[str, bool]]:
        """
        Extract a phoneme property from a condition string.

        Args:
            condition (str): The condition string.
        
        Returns:
            Dict[str, Tuple[str, bool]]: A dictionary with the property and its value.
        """
        match = re.search('\[[\+\-][a-zA-Z]+\]', condition)
        prop = None

        if match:
            positive = "+" in match.group()
            feature = match.group()[2:-1]

            if feature in BOOLEAN_PROPS:
                return {feature: (positive, positive)}

            prop = FEATURE_MAPPING.get(feature, None)

        return {prop: (feature, positive)} if prop else {}

    def _matches_phoneme(self, phoneme: str, condition: str) -> bool:
        """
        Check if a phoneme matches a condition (literal or wildcard).

        Args:
            phoneme (str): The phoneme to check.
            condition (str): The condition (literal or wildcard).

        Returns:
            bool: True if the condition matches, False otherwise.
        """
        if condition.islower():
            return phoneme == condition

        if condition in self.wildcards:
            return phoneme in self.wildcards[condition]

        if condition == 'V':
            return phoneme in VOWEL_SET

        if condition == 'C':
            return phoneme in CONSONANT_SET

        if condition in self.wildcards:
            return phoneme in self.wildcards[condition]
        
        features = self._prop_from_condition(condition)
        if features and phoneme in PHONEME_FEATURE_DICT:
            for boolean_prop in BOOLEAN_PROPS:
                if boolean_prop in features:
                    try:
                        return PHONEME_FEATURE_DICT[phoneme][boolean_prop] == features[boolean_prop][0]
                    except KeyError:
                        return False
            prop, (value, positive) = list(features.items())[0]
            if positive:
                try:
                    return PHONEME_FEATURE_DICT[phoneme][prop] == value
                except KeyError:
                    return False
            else:
                try:
                    return PHONEME_FEATURE_DICT[phoneme][prop] != value
                except KeyError:
                    return False 

        return False

    def __str__(self) -> str:
        """
        Return the string representation of the SoundChange instance.

        Returns:
            str: The string representation of the SoundChange instance.
        """
        rules = '\n'.join(
            f'{"".join(k)} > {", ".join(f"{a}" if not e else f"{a} / {e}" for a, e in v)}'
            for k, v in self.rules.items()
        )
        wildcards = '\n'.join(
            f'{k}: {" ".join(v)}'
            for k, v in self.wildcards.items()
        )
        return f'{rules}\n\n{wildcards}'

    def __repr__(self) -> str:
        """
        Return the string representation of the SoundChange instance for debugging.

        Returns:
            str: The string representation of the SoundChange instance.
        """
        return f"SoundChange(rules={self.rules}, wildcards={self.wildcards})"


class SoundChangePipeline:
    """
    A class to chain multiple sound changes together.

    Attributes:
        changes (List[SoundChange]): A list of SoundChange instances.
    """

    def __init__(self, changes: List[SoundChange]):
        """
        Initializes a SoundChangePipeline instance.

        Args:
            changes (List[SoundChange]): A list of SoundChange instances.
        """
        self.changes = changes

    def apply_to_word(self, word: Word) -> Word:
        """
        Apply all sound changes in the pipeline to a single word.

        Args:
            word (Word): The input word.

        Returns:
            Word: The mutated word.
        """
        for change in self.changes:
            word = change.apply_to_word(word)
        return word

    def apply_to_vocabulary(self, vocabulary: Vocabulary) -> Vocabulary:
        """
        Apply all sound changes in the pipeline to an entire vocabulary.

        Args:
            vocabulary (Vocabulary): The input vocabulary.

        Returns:
            Vocabulary: A new vocabulary with mutated words.
        """
        for change in self.changes:
            vocabulary = change.apply_to_vocabulary(vocabulary)
        return vocabulary

    def __str__(self) -> str:
        """
        Return the string representation of the SoundChangePipeline instance.

        Returns:
            str: The string representation of the SoundChangePipeline
        """
        return '\n\n'.join(str(change) for change in self.changes)

    def __repr__(self) -> str:
        """
        Return the string representation of the SoundChangePipeline instance for debugging.

        Returns:
            str: The string representation of the SoundChangePipeline
        """
        return f"SoundChangePipeline(changes={self.changes})"

    @staticmethod
    def random(num_changes: Optional[int] = None) -> 'SoundChangePipeline':
        """
        Generate a random SoundChangePipeline instance with random sound changes.

        Args:
            num_changes (Optional[int]): The number of sound changes to include. Defaults to a
                                         random number between 1 and 5.

        Returns:
            SoundChangePipeline: A new instance with random sound changes.
        """
        num_changes = num_changes or np.random.randint(1, 5)
        return SoundChangePipeline([SoundChange.random() for _ in range(num_changes)])

    @staticmethod
    def from_txt(file_path: str) -> 'SoundChangePipeline':
        """
        Create a SoundChangePipeline instance from a text file of rules.

        Args:
            file_path (str): The path to the file.

        Returns:
            SoundChangePipeline: A new instance with parsed sound changes.
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f'File not found: {file_path}')
        with path.open('r', encoding='utf-8') as f:
            pattern = r"(?s)(\(\w+ \d+\).*?)(?=\(\w+ \d+\)|\Z)"
            segments = re.findall(pattern, f.read())
            return SoundChangePipeline([SoundChange.from_str(segment) for segment in segments])
