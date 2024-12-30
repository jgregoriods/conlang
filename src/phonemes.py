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
