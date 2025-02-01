from typing import List, Dict, Tuple
from .phonemes import PHONEMES, COMMON_PHONEMES


def parse_phonemes(word: str) -> List[str]:
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
            for _ in range(2 if all(item in common_set for item in parse_phonemes(phoneme)) else 1)
        ]
        for category, phoneme_list in phonemes.items()
    }
    return processed


def is_acceptable(word: 'Word') -> bool:
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
        '̃': 1,   # Nasalized vowels
    }
    for char, max_count in constraints.items():
        if word.display.count(char) > max_count:
            return False

    # Prevent excessive repetition of characters
    if len(set(word.display)) < len(word.display) // 2:
        return False

    return True
