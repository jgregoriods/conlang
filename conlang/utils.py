"""
Utils Module

This module provides utility functions for processing phonemes and word patterns. It includes
functionality to parse words into phonemes, process phoneme sets to prioritize common phonemes,
and adjust patterns to prioritize simpler patterns for common words.
"""

from typing import List, Dict
from .phonemes import PHONEME_SET, COMMON_PHONEME_SET


def parse_phonemes(word: str) -> List[str]:
    """
    Splits a word string into phonemes using the predefined PHONEME_SET list.

    Args:
        word (str): The word to split into phonemes as a string.

    Returns:
        List[str]: A list of phonemes.
    """
    phonemes = []
    i = 0
    while i < len(word):
        # Phonemes can be up to 3 characters long
        for j in [3, 2, 1]:
            if word[i:i + j] in PHONEME_SET:
                phonemes.append(word[i:i + j])
                i += j
                break
        else:
            phonemes.append(word[i])
            i += 1
    return phonemes


def process_phonemes(phonemes: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Processes phoneme sets to make common phonemes more likely to be chosen.

    Args:
        phonemes (Dict[str, List[str]]): A dictionary of phoneme categories and their respective
                                         phonemes.

    Returns:
        Dict[str, List[str]]: A modified dictionary where common phonemes are more likely.
    """
    processed = {
        category: [
            phoneme for phoneme in phoneme_list
            for _ in range(2 if all(item in COMMON_PHONEME_SET for item in parse_phonemes(phoneme)) else 1)
        ]
        for category, phoneme_list in phonemes.items()
    }
    return processed


def process_patterns(patterns: List[str], phonemes: Dict[str, List[str]]) -> List[str]:
    """
    Processes patterns to prioritize simpler ones (short and without clusters).

    Args:
        patterns (List[str]): A list of patterns to process.
        phonemes (Dict[str, List[str]]): A dictionary of phoneme categories and their respective
                                         phonemes.

    Returns:
        List[str]: A modified list of patterns where simpler patterns are more likely.
    """
    def has_cluster(pattern: str) -> bool:
        """
        Checks if a pattern contains phoneme clusters.

        Args:
            pattern (str): The pattern to check.

        Returns:
            bool: True if the pattern contains clusters, False otherwise.
        """
        for letter in pattern:
            if any(char not in PHONEME_SET for char in phonemes[letter]):
                return True
        return False

    # Prioritize simpler patterns (those without clusters)
    processed = [pattern for pattern in patterns for _ in range(
        2 if not has_cluster(pattern) else 1)]
    # Sort by length to prioritize shorter patterns
    processed = sorted(processed, key=len)
    return processed
