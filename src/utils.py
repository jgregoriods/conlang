from .phonemes import PHONEMES, CONSONANTS, VOWELS


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
