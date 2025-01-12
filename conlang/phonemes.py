# Base consonants: Stops, nasals, trills, flaps, fricatives, approximants, and laterals
BASE_CONSONANTS = [
    'p', 'b', 't', 'd', 'ʈ', 'ɖ', 'c', 'ɟ', 'k', 'g', 'q', 'ɢ', 'ʔ',    # stops
    'm', 'ɱ', 'n', 'ɳ', 'ɲ', 'ŋ', 'ɴ',                                  # nasals
    'ʙ', 'r', 'ʀ',                                                      # trills
    'ⱱ', 'ɾ', 'ɽ',                                                      # taps/flaps
    'ɸ', 'β', 'f', 'v', 'θ', 'ð', 's', 'z', 'ʃ', 'ʒ', 'ʂ', 'ʐ',         # fricatives
    'ç', 'ʝ', 'x', 'ɣ', 'χ', 'ʁ', 'ħ', 'ʕ', 'h', 'ɦ',
    'ɬ', 'ɮ',                                                           # lateral fricatives
    'ʋ', 'ɹ', 'ɻ', 'j', 'ɰ',                                            # approximants
    'l', 'ɭ', 'ʎ', 'ʟ',                                                 # laterals
    'w'                                                                 # semivowels
]

# Affricates: Stops combined with fricatives
AFFRICATES = ['ts', 'dz', 'tʃ', 'dʒ', 'ʈʂ', 'ɖʐ', 'tɕ', 'dʑ', 'tɬ', 'dɮ']

# Modifiers
ASPIRATED = [f'{c}ʰ' for c in BASE_CONSONANTS + AFFRICATES]
EJECTIVES = [f'{c}ʼ' for c in BASE_CONSONANTS + AFFRICATES]
LABIALIZED = [f'{c}ʷ' for c in BASE_CONSONANTS + AFFRICATES]

# Combined consonants
CONSONANTS = BASE_CONSONANTS + AFFRICATES + ASPIRATED + EJECTIVES

# Base vowels: High, mid, and low, including rounded and unrounded variants
BASE_VOWELS = [
    'i', 'y', 'ɨ', 'ʉ', 'ɯ', 'u',   # high
    'ɪ', 'ʏ', 'ʊ',                  # near-high
    'e', 'ø', 'ɘ', 'ɵ', 'ɤ', 'o',   # mid
    'ə',                            # mid-central
    'ɛ', 'œ', 'ɜ', 'ɞ', 'ʌ', 'ɔ',   # open-mid
    'æ', 'ɐ',                       # near-open
    'a', 'ɶ', 'ä', 'ɑ', 'ɒ'         # open
]

# Long vowels
LONG_VOWELS = [f'{v}ː' for v in BASE_VOWELS]

# Combined vowels
VOWELS = BASE_VOWELS + LONG_VOWELS

# All phonemes
PHONEMES = CONSONANTS + VOWELS + ["ˈ"]

# Common phonemes: A subset of frequently used phonemes
COMMON_PHONEMES = [
    'p', 't', 'k', 'm', 'n',
    'b', 'd', 'g',
    's', 'z',
    'l', 'r',
    'i', 'u', 'e', 'o', 'a'
]
