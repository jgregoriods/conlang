import json
import numpy as np

from pathlib import Path
from typing import Dict, List, Optional
from .presets import PRESETS
from .utils import split_phonemes, split_syllables
from .phonemes import CONSONANTS


class LanguageConfig:
    """
    Represents the configuration of a language, including its phonemes, patterns, and stress rules.

    Attributes:
        phonemes (Dict[str, List[str]]): A dictionary mapping categories to phoneme lists.
        patterns (List[str]): A list of word patterns.
        stress (List[int]): A list of stress positions.
    """

    def __init__(self, phonemes: Dict[str, List[str]], patterns: List[str], stress: List[int]):
        self.phonemes = phonemes
        self.patterns = patterns
        self.stress = stress

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
            config_dict (Dict): A dictionary containing the configuration.

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
        """
        phonemes = '\n'.join(f'{k}: {" ".join(v)}' for k, v in self.phonemes.items())
        patterns = ' '.join(self.patterns)
        stress = ' '.join(map(str, self.stress))
        return f'{phonemes}\n{patterns}\n{stress}'

    def __repr__(self) -> str:
        """
        Returns a string representation of the configuration.
        """
        return self.__str__()

    @staticmethod
    def from_vocabulary(vocabulary: 'Vocabulary') -> 'LanguageConfig':
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

            phoneme_list = split_phonemes(word.replace("ˈ", ''))

            consonants_and_vowels = []
            current_chunk = [phoneme_list[0]]
            is_consonant = phoneme_list[0] in CONSONANTS

            for phoneme in phoneme_list[1:]:
                if phoneme in CONSONANTS and is_consonant:
                    current_chunk.append(phoneme)
                else:
                    consonants_and_vowels.append(current_chunk)
                    current_chunk = [phoneme]
                    is_consonant = phoneme in CONSONANTS
            consonants_and_vowels.append(current_chunk)

            for i, chunk in enumerate(consonants_and_vowels):
                first_is_consonant = chunk[0] in CONSONANTS

                # Assign key based on position and type
                # We are using Q for initial clusters, X for medial clusters,
                # Z for final clusters and N for final consonants
                if first_is_consonant:
                    if len(chunk) > 1:
                        phoneme_key = 'Q' if i == 0 else 'X' if i < len(consonants_and_vowels) - 1 else 'Z'
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

            syllables = split_syllables(word)
            for i, syllable in enumerate(syllables):
                if 'ˈ' in syllable:
                    stress_index = i - len(syllables)
                    if stress_index not in stress:
                        stress.append(stress_index)
                    break

        if 'N' in phonemes and set(phonemes['N']) == set(phonemes['C']):
            del phonemes['N']
            for i, pattern in enumerate(patterns):
                patterns[i] = pattern.replace('N', 'C')
        
        if 'Q' in phonemes and 'X' in phonemes and set(phonemes['Q']) == set(phonemes['X']):
            del phonemes['X']
            for i, pattern in enumerate(patterns):
                patterns[i] = pattern.replace('X', 'Q')

        return LanguageConfig(phonemes, patterns, stress)
