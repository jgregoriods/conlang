import numpy as np
import re

from pathlib import Path
from typing import List, Dict, Tuple, Optional
from .utils import split_phonemes, map_stress
from .vocabulary import Vocabulary
from .rules import RULES


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
        phonemes = split_phonemes(word)
        stressed = map_stress(phonemes)
        result = []

        def matches_environment(index: int, environment: str) -> bool:
            """
            Check if the phoneme at the given index matches the environment.

            Args:
                index (int): The index of the phoneme.
                environment (str): The environment string (e.g., "#_", "_#", "a_b").

            Returns:
                bool: True if the environment matches, False otherwise.
            """
            if not environment:
                return True

            if environment == "#_":
                return index == 0
            if environment == "_#":
                return index == len(phonemes) - 1

            prv, nxt = environment.split('_') if '_' in environment else (None, None)

            if prv:
                prev_idx = index - 1 if index > 0 and phonemes[index - 1] != "ˈ" else index - 2
                if prev_idx < 0 or not self._matches_phoneme(phonemes[prev_idx], prv):
                    return False

            if nxt:
                next_idx = index + 1 if index < len(phonemes) - 1 and phonemes[index + 1] != "ˈ" else index + 2
                if next_idx >= len(phonemes) or not self._matches_phoneme(phonemes[next_idx], nxt):
                    return False

            return True

        for i, phoneme in enumerate(phonemes):
            if phoneme in self.rules:
                for after, environment in self.rules[phoneme]:
                    # Handle stress-specific environments
                    if ('[+stress]' in environment and not stressed[i]) or ('[-stress]' in environment and stressed[i]):
                        continue

                    environment = environment.replace('[+stress]', '').replace('[-stress]', '').strip()

                    if matches_environment(i, environment):
                        result.append(after)
                        break
                else:
                    result.append(phoneme)
            else:
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
        rule_names = np.random.choice(
            list(RULES), size=np.random.randint(1, 6), replace=False
        )

        rules = {}
        wildcards = {}

        for rule_name in rule_names:
            rules.update(RULES[rule_name]['rules'])
            wildcards.update(RULES[rule_name]['wildcards'])

        return SoundChange(rules, wildcards)

    def _matches_phoneme(self, phoneme: str, condition: str) -> bool:
        """
        Check if a phoneme matches a condition (literal or wildcard).

        Args:
            phoneme (str): The phoneme to check.
            condition (str): The condition (literal or wildcard).

        Returns:
            bool: True if the condition matches, False otherwise.
        """
        return (
            phoneme == condition
            if condition.islower()
            else phoneme in self.wildcards.get(condition, [])
        )
