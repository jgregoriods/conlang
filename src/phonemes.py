BASE_CONSONANTS = [
    'p', 'b', 't', 'd', 'ʈ', 'ɖ', 'c', 'ɟ', 'k', 'g', 'q', 'ɢ', 'ʔ',
    'm', 'ɱ', 'n', 'ɳ', 'ɲ', 'ŋ', 'ɴ',
    'ʙ', 'r', 'ʀ',
    'ⱱ', 'ɾ', 'ɽ',
    'ɸ', 'β', 'f', 'v', 'θ', 'ð', 's', 'z', 'ʃ', 'ʒ', 'ʂ', 'ʐ', 'ç', 'ʝ', 'x', 'ɣ', 'χ', 'ʁ', 'ħ', 'ʕ', 'h', 'ɦ',
    'ɬ', 'ɮ',
    'ʋ', 'ɹ', 'ɻ', 'j', 'ɰ',
    'l', 'ɭ', 'ʎ', 'ʟ',
    'w'
]

AFFRICATES = ['ts', 'dz', 'tʃ', 'dʒ', 'ʈʂ', 'ɖʐ', 'tɕ', 'dʑ', 'tɬ', 'dɮ']
ASPIRATED = [f'{c}ʰ' for c in BASE_CONSONANTS + AFFRICATES]
EJECTIVES = [f'{c}ʼ' for c in BASE_CONSONANTS + AFFRICATES]

CONSONANTS = BASE_CONSONANTS + AFFRICATES + ASPIRATED + EJECTIVES

BASE_VOWELS = [
    'i', 'y', 'ɨ', 'ʉ', 'ɯ', 'u',
    'ɪ', 'ʏ', 'ʊ',
    'e', 'ø', 'ɘ', 'ɵ', 'ɤ', 'o',
    'ə',
    'ɛ', 'œ', 'ɜ', 'ɞ', 'ʌ', 'ɔ',
    'æ', 'ɐ',
    'a', 'ɶ', 'ä', 'ɑ', 'ɒ'
]

LONG_VOWELS = [f'{v}ː' for v in BASE_VOWELS]

VOWELS = BASE_VOWELS + LONG_VOWELS

PHONEMES = CONSONANTS + VOWELS + ["ˈ"]

COMMON_PHONEMES = [
    'p', 't', 'k', 'm', 'n',
    'b', 'd', 'g',
    's', 'z',
    'l', 'r',
    'i', 'u', 'e', 'o', 'a'
]

# For generating random presets

CONSONANT_SEED = [
    ['p', 't', 'k'],
    ['p', 't', 'tʃ', 'k'],
    ['p', 't', 'ts', 'k'],
    ['p', 't', 'k', 'q'],
]

VOWEL_SEED = [
    ['a', 'i', 'u'],
    ['a', 'e', 'i', 'o', 'u'],
    ['a', 'e', 'i', 'o', 'u', 'ɛ', 'ɔ'],
    ['a', 'e', 'i', 'o', 'u', 'y', 'ø']
]

CONSONANT_DICT = {
    'p': {'voiced': 'b', 'aspirated': 'pʰ', 'nasal': 'm', 'fricative': 'f'},
    't': {'voiced': 'd', 'aspirated': 'tʰ', 'nasal': 'n', 'fricative': 'θ'},
    'k': {'voiced': 'g', 'aspirated': 'kʰ', 'nasal': 'ŋ', 'fricative': 'x'},
    'q': {'voiced': 'ɢ', 'aspirated': 'qʰ', 'nasal': 'ɴ', 'fricative': 'χ'},
    'tʃ': {'voiced': 'dʒ', 'aspirated': 'tʃʰ', 'nasal': 'ɲ', 'fricative': 'ʃ'},
    'ts': {'voiced': 'dz', 'aspirated': 'tsʰ', 'nasal': 'n', 'fricative': 's'},
}

VOWEL_DICT = {
    'i': {'long': 'iː'},
    'u': {'long': 'uː'},
    'e': {'long': 'eː'},
    'o': {'long': 'oː'},
    'a': {'long': 'aː'},
    'ɛ': {'long': 'ɛː'},
    'ɔ': {'long': 'ɔː'},
    'y': {'long': 'yː'},
    'ø': {'long': 'øː'}
}

PATTERNS = [
    'CVCV', 'VCV', 'CV'
]

STRESS = [
    [-1], [-2], [-3],
    [-1, -2],
    [-1, -2, -3]
]

LIQUIDS = [
    ['l'], ['r'], ['l', 'r']
]

FINALS = [
    ['m', 'n', 'ŋ'],
    ['s', 'ʃ', 'z'],
    ['t', 'k', 'p'],
    ['l', 'r'],
    ['j', 'w']
]