import numpy as np
import re

from pathlib import Path
from typing import List, Dict, Tuple, Optional
from .utils import split_phonemes, get_stress_bounds
from .vocabulary import Vocabulary
from .rules import RULES
from .phonemes import VOWELS, CONSONANTS


class SoundChange:
    """
    A class to handle phonological sound changes using defined rules and wildcards.

    Attributes:
        rules (Dict[str, List[Tuple[str]]): A dictionary mapping phonemes to lists of tuples, where each tuple contains the new phoneme and the environment.
        wildcards (Optional[Dict]): A dictionary mapping wildcard symbols to lists of phonemes.
    """

    def __init__(self, rules: Dict[str, List[Tuple[str]]], wildcards: Optional[Dict] = None):
        self.rules = rules
        self.wildcards = wildcards

    def apply_to_word(self, word: str) -> str:
        """
        Apply sound changes to a single word based on defined rules.

        Args:
            word (str): The input word.

        Returns:
            str: The transformed word.
        """
        stress_start, stress_end = get_stress_bounds(word)
        phonemes = split_phonemes(word)
        result = []

        def matches_environment(index: int, environment: str) -> bool:
            """
            Check if the phoneme at the given index matches the environment.

            Args:
                index (int): The index of the phoneme.
                environment (str): The environment string (e.g., "#_", "_#", "V_V").

            Returns:
                bool: True if the environment matches, False otherwise.
            """
            if not environment:
                return True

            if environment == "#_":
                return index == 0 or index == 1 and phonemes[0] == "ˈ"
            if environment == "_#":
                return index == len(phonemes) - 1

            prv, nxt = environment.split(
                '_') if '_' in environment else (None, None)

            if prv:
                if prv == '#':
                    if index != 0 or (phonemes[0] == "ˈ" and index != 1):
                        return False

                else:
                    prev_idx = index - \
                        1 if index > 0 and phonemes[index -
                                                    1] != "ˈ" else index - 2
                    if prev_idx < 0 or not self._matches_phoneme(phonemes[prev_idx], prv):
                        return False

            if nxt:
                if nxt == '#':
                    if index != len(phonemes) - 1:
                        return False

                else:
                    next_idx = index + \
                        1 if index < len(
                            phonemes) - 1 and phonemes[index + 1] != "ˈ" else index + 2
                    if next_idx >= len(phonemes) or not self._matches_phoneme(phonemes[next_idx], nxt):
                        return False

            return True

        for i, phoneme in enumerate(phonemes):
            possible_keys = [phoneme]
            if phoneme in VOWELS and 'V' in self.rules:
                possible_keys.append('V')
            elif phoneme in CONSONANTS and 'C' in self.rules:
                possible_keys.append('C')

            matched = False

            for rule_key in possible_keys:
                if rule_key not in self.rules:
                    continue
                for after, environment in self.rules[rule_key]:
                    # Handle stress-specific environments
                    if ('[+stress]' in environment and not stress_start <= i < stress_end) or ('[-stress]' in environment and stress_start <= i < stress_end):
                        continue

                    environment = environment.replace(
                        '[+stress]', '').replace('[-stress]', '').strip()

                    if matches_environment(i, environment):
                        if 'V' in after:
                            after = after.replace(
                                'V', phoneme).replace("ː̃", "̃ː")
                        elif 'C' in after:
                            after = after.replace('C', phoneme)
                        result.append(after)
                        matched = True
                        break

                if matched:
                    break

            if not matched:
                result.append(phoneme)

        # Remove null phonemes (e.g., ∅ or 0)
        return re.sub('[∅0]', '', ''.join(result))

    def apply_to_vocabulary(self, vocabulary: Vocabulary) -> Vocabulary:
        """
        Apply sound changes to an entire vocabulary.

        Args:
            vocabulary (Vocabulary): The input vocabulary.

        Returns:
            Vocabulary: A new vocabulary with transformed words.
        """
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
            return phoneme in VOWELS

        if condition == 'C':
            return phoneme in CONSONANTS

        return False

    def __str__(self) -> str:
        """
        Return the string representation of the SoundChange instance.
        """
        rules = '\n'.join(
            f'{k} > {", ".join(f"{a}" if not e else f"{a} / {e}" for a, e in v)}'
            for k, v in self.rules.items()
        )
        wildcards = '\n'.join(
            f'{k}: {" ".join(v)}'
            for k, v in self.wildcards.items()
        )
        return f'{rules}\n\n{wildcards}'

    def __repr__(self) -> str:
        """
        Return the string representation of the SoundChange instance.
        """
        return self.__str__()


class SoundChangePipeline:
    """
    A class to chain multiple sound changes together.

    Attributes:
        changes (List[SoundChange]): A list of SoundChange instances.
    """

    def __init__(self, changes: List[SoundChange]):
        self.changes = changes

    def apply_to_word(self, word: str) -> str:
        """
        Apply all sound changes in the pipeline to a single word.

        Args:
            word (str): The input word.

        Returns:
            str: The transformed word.
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
            Vocabulary: A new vocabulary with transformed words.
        """
        for change in self.changes:
            vocabulary = change.apply_to_vocabulary(vocabulary)
        return vocabulary

    def __str__(self) -> str:
        """
        Return the string representation of the SoundChangePipeline instance.
        """
        return '\n'.join(str(change) for change in self.changes)

    def __repr__(self) -> str:
        """
        Return the string representation of the SoundChangePipeline instance.
        """
        return self.__str__()

    @staticmethod
    def random(num_changes: Optional[int] = None) -> 'SoundChangePipeline':
        """
        Generate a random SoundChangePipeline instance with random sound changes.

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
