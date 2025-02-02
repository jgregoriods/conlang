"""
Language Module

This module provides functionality to generate and manage languages, including their vocabulary,
word generation, and configuration. The main class, `Language`, represents a language and provides
methods for generating words, building vocabulary, and creating languages from existing
vocabularies.
"""

import warnings
from typing import List, Optional
import numpy as np
from .language_config import LanguageConfig
from .swadesh import SWADESH
from .vocabulary import Vocabulary
from .word import Word


MAX_ATTEMPTS = 10


class Language:
    """
    Represents a language, including its configuration and vocabulary.

    Attributes:
        name (str): The name of the language.
        config (LanguageConfig): The configuration for phonemes, word patterns, and stress.
        vocabulary (Vocabulary): The generated vocabulary for the language.
    """

    def __init__(self, name: str, config: LanguageConfig, vocabulary: Optional[Vocabulary] = None):
        """
        Initializes a Language instance.

        Args:
            name (str): The name of the language.
            config (LanguageConfig): The configuration for phonemes, patterns, and stress.
            vocabulary (Vocabulary, optional): The vocabulary for the language. Defaults to an
                                               empty Vocabulary.
        """
        self.name = name
        self.config = config
        self.vocabulary = vocabulary or Vocabulary()

    def generate_word(self, rank: int = -1) -> str:
        """
        Generates a word based on the language's configuration and word frequency rank.

        Args:
            rank (int): The rank of the word for frequency purposes. Common words (rank < 25)
                        use simpler patterns. Defaults to -1.

        Returns:
            str: The generated word.
        """
        # Select a pattern based on rank (common words have simpler patterns)
        patterns = self.config.short_patterns if 0 <= rank < 25 else self.config.patterns_weighted
        pattern = np.random.choice(patterns)

        # Generate the word by selecting random phonemes for each category in the pattern
        word = Word(''.join(np.random.choice(
            self.config.phonemes_weighted[k]) for k in pattern))

        # Assign stress to the word
        stressed_index = np.random.choice(self.config.stress)
        word.set_stress(stressed_index)

        return word

    def generate_vocabulary(self, glosses: Optional[List[str]] = None):
        """
        Generates a vocabulary for the language based on glosses.

        Args:
            glosses (List[str], optional): A list of glosses to use for the vocabulary. 
                                           Defaults to the SWADESH list.
        """
        self.vocabulary = Vocabulary()

        # Use the SWADESH list if no glosses are provided
        glosses = glosses or SWADESH

        for gloss in glosses:
            rank = SWADESH.index(gloss) if gloss in SWADESH else -1
            attempts = 0

            # Generate a unique and acceptable word for the gloss
            while attempts < MAX_ATTEMPTS:
                word = self.generate_word(rank=rank)
                if word.is_acceptable() and not self.vocabulary.has_word(word):
                    break
                attempts += 1

            # Add the word to the vocabulary
            self.vocabulary.add_item(word, gloss)

            # Warn if a unique acceptable word could not be generated
            if attempts == MAX_ATTEMPTS:
                warnings.warn(
                    f"Failed to generate unique acceptable word for '{gloss}'. "
                    "Please, check your configuration."
                )

    def __str__(self) -> str:
        """
        Returns a string representation of the language.

        Returns:
            str: A formatted string showing the language name, configuration, and vocabulary.
        """
        return f"{self.name}\n\n{self.config}\n\n{self.vocabulary}"

    def __repr__(self):
        """
        Returns a string representation of the language for debugging.

        Returns:
            str: A string representation of the Language instance.
        """
        return f"Language(name={self.name}, config={self.config}, vocabulary={self.vocabulary})"

    @staticmethod
    def from_vocabulary(name: str, vocabulary: Vocabulary) -> 'Language':
        """
        Create a new Language instance from an existing vocabulary.

        Args:
            name (str): The name of the language.
            vocabulary (Vocabulary): The vocabulary for the language.

        Returns:
            Language: A new Language instance with a configuration derived from the vocabulary.
        """
        config = LanguageConfig.from_vocabulary(vocabulary)
        return Language(name, config, vocabulary)
