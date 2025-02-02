"""
Language Configuration Module

This module provides functionality to define, load, and manipulate language configurations,
including phonemes, word patterns, and stress rules. It supports loading configurations from
strings, text files, JSON files, and presets, as well as detecting the configuration from a
vocabulary.
"""

import json
from pathlib import Path
from typing import Dict, List
import numpy as np
from .phonemes import CONSONANT_SET
from .presets import PRESETS
from .vocabulary import Vocabulary
from .utils import process_phonemes, process_patterns


class LanguageConfig:
    """
    Represents the configuration of a language, including its phonemes, word patterns, and stress
    rules.

    Attributes:
        phonemes (Dict[str, List[str]]): A dictionary mapping phoneme categories to lists of
                                         phonemes.
        patterns (List[str]): A list of word patterns, where each pattern is a sequence of phoneme
                              categories.
        stress (List[int]): A list of stressed syllable positions (as negative indices).
    """

    def __init__(self, phonemes: Dict[str, List[str]], patterns: List[str], stress: List[int]):
        """
        Initializes a LanguageConfig instance.

        Args:
            phonemes (Dict[str, List[str]]): A dictionary mapping phoneme categories to lists of
                                             phonemes.
            patterns (List[str]): A list of word patterns.
            stress (List[int]): A list of stress positions.
            phonemes_weighted (Dict[str, List[str]]): A dictionary where common phonemes are more
                                                      likely to be chosen.
            patterns_weighted (List[str]): A list of word patterns with simple patterns more likely.
            short_patterns (List[str]): A list of the shortest patterns.
        """
        self.phonemes = phonemes
        self.patterns = sorted(patterns, key=len)
        self.stress = stress
        self.phonemes_weighted = process_phonemes(phonemes)
        self.patterns_weighted = process_patterns(patterns, phonemes)
        self.short_patterns = self.patterns_weighted[:len(
            self.patterns_weighted) // 2] if len(self.patterns_weighted) > 1 else self.patterns_weighted

    @staticmethod
    def from_str(config_str: str) -> 'LanguageConfig':
        """
        Parses a configuration string to create a LanguageConfig instance.

        Args:
            config_str (str): The configuration as a multi-line string.

        Returns:
            LanguageConfig: The parsed language configuration.
        """
        phonemes = {}
        patterns = []
        stress = []

        for line in config_str.splitlines():
            line = line.strip()
            if not line:
                continue
            if ':' in line:
                key, values = line.split(':')
                phonemes[key.strip()] = values.strip().split()
            elif line.replace('-', '').replace(' ', '').isdigit():
                stress.extend(map(int, line.split()))
            elif line.isupper():
                patterns.extend(line.split())
            else:
                raise ValueError(f'Invalid line in configuration: {line}')

        return LanguageConfig(phonemes, patterns, stress)

    @staticmethod
    def from_txt(file_path: str) -> 'LanguageConfig':
        """
        Reads a configuration from a text file to create a LanguageConfig instance.

        Args:
            file_path (str): The path to the configuration file.

        Returns:
            LanguageConfig: The parsed language configuration.
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f'File not found: {file_path}')
        with path.open('r', encoding='utf-8') as f:
            return LanguageConfig.from_str(f.read())

    @staticmethod
    def from_dict(config_dict: Dict) -> 'LanguageConfig':
        """
        Creates a LanguageConfig instance from a dictionary.

        Args:
            config_dict (Dict): A dictionary containing the configuration with keys 'phonemes',
                                'patterns', and 'stress'.

        Returns:
            LanguageConfig: The parsed language configuration.
        """
        return LanguageConfig(
            phonemes=config_dict['phonemes'],
            patterns=config_dict['patterns'],
            stress=config_dict['stress']
        )

    @staticmethod
    def from_json(file_path: str) -> 'LanguageConfig':
        """
        Reads a configuration from a JSON file to create a LanguageConfig instance.

        Args:
            file_path (str): The path to the configuration file.

        Returns:
            LanguageConfig: The parsed language configuration.
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f'File not found: {file_path}')
        with path.open('r', encoding='utf-8') as f:
            return LanguageConfig.from_dict(json.load(f))

    @staticmethod
    def random() -> 'LanguageConfig':
        """
        Generates a random LanguageConfig instance using predefined presets.

        Returns:
            LanguageConfig: A randomly selected language configuration.
        """
        preset_key = np.random.choice(list(PRESETS.keys()))
        preset = PRESETS[preset_key]
        return LanguageConfig(
            phonemes=preset['phonemes'],
            patterns=preset['patterns'],
            stress=preset['stress']
        )

    @staticmethod
    def load_preset(name: str) -> 'LanguageConfig':
        """
        Loads a language configuration preset by name.

        Args:
            name (str): The name of the preset to load.

        Returns:
            LanguageConfig: The language configuration preset.
        """
        if name not in PRESETS:
            raise ValueError(f'Preset not found: {name}')
        preset = PRESETS[name]
        return LanguageConfig(
            phonemes=preset['phonemes'],
            patterns=preset['patterns'],
            stress=preset['stress']
        )

    def __str__(self) -> str:
        """
        Returns a string representation of the configuration.

        Returns:
            str: A formatted string showing phonemes, patterns, and stress.
        """
        phonemes = '\n'.join(f'{k}: {" ".join(v)}' for k,
                             v in self.phonemes.items())
        patterns = ' '.join(self.patterns)
        stress = ' '.join(map(str, self.stress))
        return f'{phonemes}\n{patterns}\n{stress}'

    def __repr__(self) -> str:
        """
        Returns a string representation of the configuration for debugging.

        Returns:
            str: A string representation of the LanguageConfig instance.
        """
        return f'LanguageConfig(phonemes={self.phonemes}, patterns={self.patterns}, stress={self.stress})'

    @staticmethod
    def from_vocabulary(vocabulary: Vocabulary) -> 'LanguageConfig':
        """
        Generates a language configuration from a vocabulary.

        Args:
            vocabulary (Vocabulary): The vocabulary to generate the configuration from.

        Returns:
            LanguageConfig: The generated language configuration.
        """
        phonemes = {}
        patterns = []
        stress = []

        for item in vocabulary.items:
            word = item['word']
            word_pattern = ''

            phoneme_list = word.phonemes

            consonants_and_vowels = []
            current_chunk = [phoneme_list[0]]
            is_consonant = phoneme_list[0] in CONSONANT_SET

            for phoneme in phoneme_list[1:]:
                if phoneme in CONSONANT_SET and is_consonant:
                    current_chunk.append(phoneme)
                else:
                    consonants_and_vowels.append(current_chunk)
                    current_chunk = [phoneme]
                    is_consonant = phoneme in CONSONANT_SET
            consonants_and_vowels.append(current_chunk)

            for i, chunk in enumerate(consonants_and_vowels):
                first_is_consonant = chunk[0] in CONSONANT_SET

                # Assign key based on position and type
                # We are using Q for initial clusters, X for medial clusters,
                # Z for final clusters and N for final consonants
                if first_is_consonant:
                    if len(chunk) > 1:
                        phoneme_key = 'Q' if i == 0 else 'X' if i < len(
                            consonants_and_vowels) - 1 else 'Z'
                    elif i == len(consonants_and_vowels) - 1:
                        phoneme_key = 'N'
                    else:
                        phoneme_key = 'C'
                else:
                    phoneme_key = 'V'

                word_pattern += phoneme_key

                phoneme_str = ''.join(chunk)
                if phoneme_key not in phonemes:
                    phonemes[phoneme_key] = []
                if phoneme_str not in phonemes[phoneme_key]:
                    phonemes[phoneme_key].append(phoneme_str)

            if word_pattern not in patterns:
                patterns.append(word_pattern)

            if word.stress not in stress:
                stress.append(word.stress)

        # Simplify phoneme categories if redundant
        if 'N' in phonemes and set(phonemes['N']) == set(phonemes['C']):
            del phonemes['N']
            patterns = [pattern.replace('N', 'C') for pattern in patterns]

        if 'Q' in phonemes and 'X' in phonemes and set(phonemes['Q']) == set(phonemes['X']):
            del phonemes['X']
            patterns = [pattern.replace('X', 'Q') for pattern in patterns]

        return LanguageConfig(phonemes, patterns, stress)
