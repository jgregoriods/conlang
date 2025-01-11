from .phonemes import PHONEMES, CONSONANTS, VOWELS, COMMON_PHONEMES


def split_phonemes(word: str) -> list:
    res = []
    i = 0
    while i < len(word):
        for j in [3, 2, 1]:
            if word[i:i + j] in PHONEMES:
                res.append(word[i:i + j])
                i += j
                break
        else:
            res.append(word[i])
            i += 1
    return res


def split_syllables(word: str) -> list:
    """
    Splits a word into syllables.
    """
    phonemes = split_phonemes(word)
    syllables = []
    current = ''
    for p in phonemes:
        current += p
        if p in VOWELS:
            syllables.append(current)
            current = ''
    if current:
        syllables[-1] += current
    return syllables


def map_stress(phonemes: list) -> list:
    """
    Maps the stress markers to the phonemes.
    """
    if len(set(VOWELS) & set(phonemes)) == 1:
        return [True] * len(phonemes)
    stress = [False] * len(phonemes)
    for i, phoneme in enumerate(phonemes):
        if phoneme == "ˈ":
            stress[i + 1] = True
            j = i + 2
            while j < len(phonemes) and phonemes[j] not in CONSONANTS:
                stress[j] = True
                j += 1
    return stress


def process_phonemes(phonemes: dict) -> dict:
    # we will cheat a bit to make the common phonemes more likely
    # to be chosen
    res = {}
    for k, v in phonemes.items():
        p = []
        for x in v:
            p.extend([x] * (2 if x in COMMON_PHONEMES else 1))
        res[k] = p
    return res


def is_acceptable(word: str) -> bool:
    """
    Checks if the given word is acceptable.
    """

    # allow only one aspirated consonant
    if word.count('ʰ') > 1:
        return False

    # allow only one ejective consonant
    if word.count('ʼ') > 1:
        return False

    # allow only one long vowel
    if word.count('ː') > 1:
        return False

    # allow only one labialized consonant
    if word.count('ʷ') > 1:
        return False

    # prevent too many repeated characters
    if len(set(word)) < len(word) // 2:
        return False

    return True