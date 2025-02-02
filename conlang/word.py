"""
Word Module

This module provides functionality to represent and manipulate words. The main class, `Word`,
handles the parsing of phonemes, syllable splitting, stress, and display formatting.
"""

from typing import List, Tuple
from .phonemes import VOWEL_SET, CONSONANT_SET
from .utils import parse_phonemes


class Word:
    """
    Represents a word with its phonemes, syllables, and stress information.

    Attributes:
        word_str (str): The original string representation of the word.
        display (str): The formatted display string.
        stress (Optional[int]): The stressed syllable position (as a negative index).
        phonemes (List[str]): The list of phonemes in the word.
        syllables (List[List[str]]): The list of syllables, each represented as a list of phonemes.
        stress_bounds (Tuple[int, int]): The start and end indices of the stressed phonemes.
    """

    def __init__(self, word_str: str):
        """
        Initializes a Word instance.

        Args:
            word_str (str): The string representation of the word.
        """
        self.word_str = word_str
        self.display = word_str
        self.stress = None
        self.phonemes = parse_phonemes(word_str)
        self.syllables = self.split_syllables()
        self.stress_bounds = self.get_stress_bounds()

        self.update_display()

    def split_syllables(self) -> List[List[str]]:
        """
        Splits the word into syllables based on phonemes.

        Args:
            phonemes (List[str]): The list of phonemes in the word.

        Returns:
            List[List[str]]: A list of syllables, each represented as a list of phonemes.
        """
        syllables = []
        current_syllable = []

        for phoneme in self.phonemes:
            current_syllable.append(phoneme)
            if phoneme in VOWEL_SET:
                syllables.append(current_syllable)
                current_syllable = []

        if current_syllable:
            if syllables:
                syllables[-1].extend(current_syllable)
            else:
                syllables.append(current_syllable)

        # Adjust consonant clusters across syllable boundaries
        adjusted_syllables = []
        for i, syllable in enumerate(syllables):
            if i > 0 and len(syllable) > 1 and syllable[0] in CONSONANT_SET and syllable[1] in CONSONANT_SET:
                # Move the leading consonant to the previous syllable
                adjusted_syllables[-1].append(syllable.pop(0))
            adjusted_syllables.append(syllable)

        # Identify stress position
        for i, syllable in enumerate(adjusted_syllables):
            if "ˈ" in syllable:
                self.stress = i - len(adjusted_syllables)
                break

        return adjusted_syllables

    def update_display(self) -> None:
        """
        Updates the display string.
        """
        for syllable in self.syllables:
            if "ˈ" in syllable:
                syllable.remove("ˈ")
                break
        if "ˈ" in self.phonemes:
            self.phonemes.remove("ˈ")

        if self.stress is not None:
            # Insert stress marker in the correct syllable
            stressed_index = len(self.syllables) + self.stress
            syllables = [syl.copy() for syl in self.syllables]
            syllables[stressed_index].insert(0, "ˈ")
            self.display = "".join("".join(syl) for syl in syllables)
        else:
            self.display = "".join("".join(syl) for syl in self.syllables)

    def set_stress(self, stress: int) -> None:
        """
        Sets the stress position for the word.

        Args:
            stress (int): The stressed syllable position as a negative index.
        """
        self.stress = max(stress, -len(self.syllables))
        self.stress_bounds = self.get_stress_bounds()
        self.update_display()

    def __str__(self) -> str:
        """
        Returns the formatted display string of the word.

        Returns:
            str: formatted display string of the word.
        """
        return self.display

    def __repr__(self) -> str:
        """
        Returns the string representation of the Word instance for debugging.

        Returns:
            str: The string representation of the Word instance.
        """
        return f"Word({self.display})"

    def __eq__(self, other: 'Word') -> bool:
        """
        Compares two Word instances for equality based on their phonemes and stress.

        Args:
            other (Word): The other Word instance to compare.

        Returns:
            bool: True if the phonemes and stress are equal, False otherwise.
        """
        return self.phonemes == other.phonemes and self.stress == other.stress

    def get_stress_bounds(self) -> Tuple[int, int]:
        """
        Determines the start and end indices of the stressed phonemes.

        Returns:
            Tuple[int, int]: The start and end indices of the stressed phonemes.
                             Returns None if no stress is set.
        """
        if self.stress is None:
            return None

        start = end = 0

        for i, syllable in enumerate(self.syllables):
            start = end
            end += len(syllable)
            if i == len(self.syllables) + self.stress:
                break

        return start, end

    def is_acceptable(self) -> bool:
        """
        Determines whether a word is acceptable based on specific phonetic constraints.

        Returns:
            bool: True if the word is acceptable, False otherwise.
        """
        # Constraints on specific phonetic elements
        constraints = {
            'ʰ': 1,  # Aspirated consonants
            'ʼ': 1,  # Ejective consonants
            'ː': 1,  # Long vowels
            'ʷ': 1,  # Labialized consonants
            '̃': 1,   # Nasalized vowels
        }
        for char, max_count in constraints.items():
            if self.display.count(char) > max_count:
                return False

        # Prevent excessive repetition of characters
        if len(set(self.display)) < len(self.display) // 2:
            return False

        return True
