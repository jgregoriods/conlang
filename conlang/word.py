from typing import List, Tuple
from .phonemes import VOWELS, CONSONANTS
from .utils import parse_phonemes


class Word:
    def __init__(self, word_str: str):
        self.word_str = word_str
        self.display = word_str
        self.stress = None
        self.phonemes = parse_phonemes(word_str)
        self.syllables = self.split_syllables(self.phonemes)
        self.stress_bounds = self.get_stress_bounds()

        self.update_display()

    def split_syllables(self, phonemes):
        syllables = []
        current_syllable = []

        for phoneme in phonemes:
            current_syllable.append(phoneme)
            if phoneme in VOWELS:
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
            if i > 0 and len(syllable) > 1 and syllable[0] in CONSONANTS and syllable[1] in CONSONANTS:
                # Move the leading consonant to the previous syllable
                adjusted_syllables[-1].append(syllable.pop(0))
            adjusted_syllables.append(syllable)

        for i, syllable in enumerate(adjusted_syllables):
            if "ˈ" in syllable:
                self.stress = i - len(adjusted_syllables)
                break

        return adjusted_syllables

    def update_display(self):
        for syllable in self.syllables:
            if "ˈ" in syllable:
                syllable.remove("ˈ")
                break
        if "ˈ" in self.phonemes:
            self.phonemes.remove("ˈ")

        if self.stress is None:
            return

        stressed_index = len(self.syllables) + self.stress
        syllables = [syl.copy() for syl in self.syllables]
        syllables[stressed_index].insert(0, "ˈ")
        self.display = "".join("".join(syl) for syl in syllables)

    def set_stress(self, stress: int):
        self.stress = max(stress, -len(self.syllables))
        self.stress_bounds = self.get_stress_bounds()
        self.update_display()

    def __str__(self):
        return self.display

    def __repr__(self):
        return self.display

    def __eq__(self, other):
        return self.phonemes == other.phonemes

    def get_stress_bounds(self) -> Tuple[int, int]:
        """
        Maps which phonemes are in a stressed syllable.

        Returns:
            List[bool]: A list indicating stressed (True) and unstressed (False) phonemes.
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
