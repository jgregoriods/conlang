import json
import numpy as np

from pathlib import Path
from typing import Dict, List
from .presets import PRESETS


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
        preset_key = np.random.choice(list(PRESETS))
        preset = PRESETS[preset_key]
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
