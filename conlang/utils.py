from typing import List, Dict
from .phonemes import PHONEMES, CONSONANTS, VOWELS, COMMON_PHONEMES


def split_phonemes(word: str) -> List[str]:
    """
    Splits a word into phonemes using the predefined PHONEMES list.

    Args:
        word (str): The word to split into phonemes.

    Returns:
        List[str]: A list of phonemes.
    """
    phonemes = []
    i = 0
    while i < len(word):
        # Phonemes can be up to 3 characters long
        for j in [3, 2, 1]:
            if word[i:i + j] in PHONEMES:
                phonemes.append(word[i:i + j])
                i += j
                break
        else:
            phonemes.append(word[i])
            i += 1
    return phonemes


def split_syllables(word: str) -> List[str]:
    """
    Splits a word into syllables.

    Args:
        word (str): The word to split into syllables.

    Returns:
        List[str]: A list of syllables.
    """
    phonemes = split_phonemes(word)
    syllables = []
    current_syllable = ''

    for phoneme in phonemes:
        current_syllable += phoneme
        if phoneme in VOWELS:
            syllables.append(current_syllable)
            current_syllable = ''

    if current_syllable:
        if syllables:
            syllables[-1] += current_syllable
        else:
            syllables.append(current_syllable)

    return syllables


def map_stress(word: str) -> List[bool]:
    """
    Maps which phonemes are in a stressed syllable.

    Args:
        phonemes (List[str]): A list of phonemes.

    Returns:
        List[bool]: A list indicating stressed (True) and unstressed (False) phonemes.
    """
    syllables = split_syllables(word)
    stressed = []
    for syllable in syllables:
        if 'ˈ' in syllable:
            stressed.extend([True] * len(syllable))
        else:
            stressed.extend([False] * len(syllable))
    return stressed


def process_phonemes(phonemes: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Processes phoneme sets to make common phonemes more likely to be chosen.

    Args:
        phonemes (Dict[str, List[str]]): A dictionary of phoneme categories and their respective phonemes.

    Returns:
        Dict[str, List[str]]: A modified dictionary where common phonemes are more likely.
    """
    common_set = set(COMMON_PHONEMES)  # Convert to set for faster lookup
    processed = {
        category: [
            phoneme for phoneme in phoneme_list
            for _ in range(2 if all(item in common_set for item in split_phonemes(phoneme)) else 1)
        ]
        for category, phoneme_list in phonemes.items()
    }
    return processed


def is_acceptable(word: str) -> bool:
    """
    Determines whether a word is acceptable based on specific phonetic constraints.

    Args:
        word (str): The word to validate.

    Returns:
        bool: True if the word is acceptable, False otherwise.
    """
    # Constraints on specific phonetic elements
    constraints = {
        'ʰ': 1,  # Aspirated consonants
        'ʼ': 1,  # Ejective consonants
        'ː': 1,  # Long vowels
        'ʷ': 1,  # Labialized consonants
    }
    for char, max_count in constraints.items():
        if word.count(char) > max_count:
            return False

    # Prevent excessive repetition of characters
    if len(set(word)) < len(word) // 2:
        return False

    return True
