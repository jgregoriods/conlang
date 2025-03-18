# Base consonants: Stops, nasals, trills, flaps, fricatives, approximants, and laterals
BASE_CONSONANTS = [
    'p', 'b', 't', 'd', 'ʈ', 'ɖ', 'c', 'ɟ', 'k', 'g', 'q', 'ɢ', 'ʔ',    # stops
    'm', 'ɱ', 'n', 'ɳ', 'ɲ', 'ŋ', 'ɴ',                                  # nasals
    'ʙ', 'r', 'ʀ',                                                      # trills
    'ⱱ', 'ɾ', 'ɽ',                                                      # taps/flaps
    'ɸ', 'β', 'f', 'v', 'θ', 'ð', 's', 'z', 'ʃ', 'ʒ', 'ʂ', 'ʐ',         # fricatives
    'ɕ', 'ʑ', 'ç', 'ʝ', 'x', 'ɣ', 'χ', 'ʁ', 'ħ', 'ʕ', 'h', 'ɦ',
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
CONSONANTS = BASE_CONSONANTS + AFFRICATES + ASPIRATED + EJECTIVES + LABIALIZED

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
NASAL_VOWELS = [f'{v}̃' for v in BASE_VOWELS]
LONG_VOWELS = [f'{v}ː' for v in BASE_VOWELS + NASAL_VOWELS]

# Combined vowels
VOWELS = BASE_VOWELS + LONG_VOWELS + NASAL_VOWELS

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

# For faster lookups
PHONEME_SET = set(PHONEMES)
COMMON_PHONEME_SET = set(COMMON_PHONEMES)
VOWEL_SET = set(VOWELS)
CONSONANT_SET = set(CONSONANTS)

PLACES = {'bilabial', 'labiodental', 'dental', 'alveolar', 'postalveolar', 'retroflex', 'palatal', 'velar', 'uvular', 'pharyngeal', 'glottal'}
MANNERS = {'stop', 'nasal', 'trill', 'tap', 'fricative', 'lateral fricative', 'approximant'}
HEIGHTS = {'close', 'near-close', 'close-mid', 'mid', 'open-mid', 'near-open', 'open'}
BACKNESSES = {'front', 'central', 'back'}
BOOLEAN_PROPS = {'voiced', 'labialized', 'aspirated', 'ejective', 'rounded', 'nasalized', 'long'}

FEATURE_MAPPING = {
    **{f: 'manner' for f in MANNERS},
    **{f: 'place' for f in PLACES},
    **{f: 'height' for f in HEIGHTS},
    **{f: 'backness' for f in BACKNESSES},
}

# Feature notation
PHONEME_FEATURE_DICT = {
    'p': {'place': 'bilabial', 'manner': 'stop', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'b': {'place': 'bilabial', 'manner': 'stop', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    't': {'place': 'alveolar', 'manner': 'stop', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'd': {'place': 'alveolar', 'manner': 'stop', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ʈ': {'place': 'retroflex', 'manner': 'stop', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ɖ': {'place': 'retroflex', 'manner': 'stop', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'c': {'place': 'palatal', 'manner': 'stop', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ɟ': {'place': 'palatal', 'manner': 'stop', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'k': {'place': 'velar', 'manner': 'stop', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'g': {'place': 'velar', 'manner': 'stop', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'q': {'place': 'uvular', 'manner': 'stop', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ɢ': {'place': 'uvular', 'manner': 'stop', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ʔ': {'place': 'glottal', 'manner': 'stop', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'm': {'place': 'bilabial', 'manner': 'nasal', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ɱ': {'place': 'labiodental', 'manner': 'nasal', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'n': {'place': 'alveolar', 'manner': 'nasal', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ɳ': {'place': 'retroflex', 'manner': 'nasal', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ɲ': {'place': 'palatal', 'manner': 'nasal', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ŋ': {'place': 'velar', 'manner': 'nasal', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ɴ': {'place': 'uvular', 'manner': 'nasal', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ʙ': {'place': 'bilabial', 'manner': 'trill', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'r': {'place': 'alveolar', 'manner': 'trill', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ʀ': {'place': 'uvular', 'manner': 'trill', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ⱱ': {'place': 'labiodental', 'manner': 'tap', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ɾ': {'place': 'alveolar', 'manner': 'tap', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ɽ': {'place': 'retroflex', 'manner': 'tap', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ɸ': {'place': 'bilabial', 'manner': 'fricative', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'β': {'place': 'bilabial', 'manner': 'fricative', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'f': {'place': 'labiodental', 'manner': 'fricative', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'v': {'place': 'labiodental', 'manner': 'fricative', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'θ': {'place': 'dental', 'manner': 'fricative', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ð': {'place': 'dental', 'manner': 'fricative', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    's': {'place': 'alveolar', 'manner': 'fricative', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'z': {'place': 'alveolar', 'manner': 'fricative', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ʃ': {'place': 'postalveolar', 'manner': 'fricative', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ʒ': {'place': 'postalveolar', 'manner': 'fricative', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ʂ': {'place': 'retroflex', 'manner': 'fricative', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ʐ': {'place': 'retroflex', 'manner': 'fricative', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ɕ': {'place': 'alveolopalatal', 'manner': 'fricative', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ʑ': {'place': 'alveolopalatal', 'manner': 'fricative', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ç': {'place': 'palatal', 'manner': 'fricative', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ʝ': {'place': 'palatal', 'manner': 'fricative', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'x': {'place': 'velar', 'manner': 'fricative', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ɣ': {'place': 'velar', 'manner': 'fricative', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'χ': {'place': 'uvular', 'manner': 'fricative', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ʁ': {'place': 'uvular', 'manner': 'fricative', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ħ': {'place': 'pharyngeal', 'manner': 'fricative', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ʕ': {'place': 'pharyngeal', 'manner': 'fricative', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'h': {'place': 'glottal', 'manner': 'fricative', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ɦ': {'place': 'glottal', 'manner': 'fricative', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ɬ': {'place': 'alveolar', 'manner': 'lateral fricative', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ɮ': {'place': 'alveolar', 'manner': 'lateral fricative', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ʋ': {'place': 'labiodental', 'manner': 'approximant', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ɹ': {'place': 'alveolar', 'manner': 'approximant', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ɻ': {'place': 'retroflex', 'manner': 'approximant', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'j': {'place': 'palatal', 'manner': 'approximant', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ɰ': {'place': 'velar', 'manner': 'approximant', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'l': {'place': 'alveolar', 'manner': 'lateral approximant', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ɭ': {'place': 'retroflex', 'manner': 'lateral approximant', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ʎ': {'place': 'palatal', 'manner': 'lateral approximant', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ʟ': {'place': 'velar', 'manner': 'lateral approximant', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'w': {'place': 'labial-velar', 'manner': 'approximant', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ts': {'place': 'alveolar', 'manner': 'affricate', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'dz': {'place': 'alveolar', 'manner': 'affricate', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'tʃ': {'place': 'postalveolar', 'manner': 'affricate', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'dʒ': {'place': 'postalveolar', 'manner': 'affricate', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ʈʂ': {'place': 'retroflex', 'manner': 'affricate', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'ɖʐ': {'place': 'retroflex', 'manner': 'affricate', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'tɕ': {'place': 'alveolopalatal', 'manner': 'affricate', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'dʑ': {'place': 'alveolopalatal', 'manner': 'affricate', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'tɬ': {'place': 'alveolar', 'manner': 'lateral affricate', 'voiced': False, 'labialized': False, 'aspirated': False, 'ejective': False},
    'dɮ': {'place': 'alveolar', 'manner': 'lateral affricate', 'voiced': True, 'labialized': False, 'aspirated': False, 'ejective': False},
    'i': {'height': 'close', 'backness': 'front', 'rounded': False, 'nasalized': False, 'long': False},
    'y': {'height': 'close', 'backness': 'front', 'rounded': True, 'nasalized': False, 'long': False},
    'ɨ': {'height': 'close', 'backness': 'central', 'rounded': False, 'nasalized': False, 'long': False},
    'ʉ': {'height': 'close', 'backness': 'central', 'rounded': True, 'nasalized': False, 'long': False},
    'ɯ': {'height': 'close', 'backness': 'back', 'rounded': False, 'nasalized': False, 'long': False},
    'u': {'height': 'close', 'backness': 'back', 'rounded': True, 'nasalized': False, 'long': False},
    'ɪ': {'height': 'near-close', 'backness': 'front', 'rounded': False, 'nasalized': False, 'long': False},
    'ʏ': {'height': 'near-close', 'backness': 'front', 'rounded': True, 'nasalized': False, 'long': False},
    'ʊ': {'height': 'near-close', 'backness': 'back', 'rounded': True, 'nasalized': False, 'long': False},
    'e': {'height': 'close-mid', 'backness': 'front', 'rounded': False, 'nasalized': False, 'long': False},
    'ø': {'height': 'close-mid', 'backness': 'front', 'rounded': True, 'nasalized': False, 'long': False},
    'ɘ': {'height': 'close-mid', 'backness': 'central', 'rounded': False, 'nasalized': False, 'long': False},
    'ɵ': {'height': 'close-mid', 'backness': 'central', 'rounded': True, 'nasalized': False, 'long': False},
    'ɤ': {'height': 'close-mid', 'backness': 'back', 'rounded': False, 'nasalized': False, 'long': False},
    'o': {'height': 'close-mid', 'backness': 'back', 'rounded': True, 'nasalized': False, 'long': False},
    'ə': {'height': 'mid', 'backness': 'central', 'rounded': False, 'nasalized': False, 'long': False},
    'ɛ': {'height': 'open-mid', 'backness': 'front', 'rounded': False, 'nasalized': False, 'long': False},
    'œ': {'height': 'open-mid', 'backness': 'front', 'rounded': True, 'nasalized': False, 'long': False},
    'ɜ': {'height': 'open-mid', 'backness': 'central', 'rounded': False, 'nasalized': False, 'long': False},
    'ɞ': {'height': 'open-mid', 'backness': 'central', 'rounded': True, 'nasalized': False, 'long': False},
    'ʌ': {'height': 'open-mid', 'backness': 'back', 'rounded': False, 'nasalized': False, 'long': False},
    'ɔ': {'height': 'open-mid', 'backness': 'back', 'rounded': True, 'nasalized': False, 'long': False},
    'æ': {'height': 'near-open', 'backness': 'front', 'rounded': False, 'nasalized': False, 'long': False},
    'ɐ': {'height': 'near-open', 'backness': 'central', 'rounded': False, 'nasalized': False, 'long': False},
    'a': {'height': 'open', 'backness': 'front', 'rounded': False, 'nasalized': False, 'long': False},
    'ɶ': {'height': 'open', 'backness': 'front', 'rounded': True, 'nasalized': False, 'long': False},
    'ɑ': {'height': 'open', 'backness': 'back', 'rounded': False, 'nasalized': False, 'long': False},
    'ɒ': {'height': 'open', 'backness': 'back', 'rounded': True, 'nasalized': False, 'long': False},
}

PHONEME_FEATURE_DICT.update({
    f'{c}ʰ': {'place': features['place'], 'manner': features['manner'], 'voiced': features['voiced'], 'labialized': features['labialized'], 'aspirated': True, 'ejective': False}
    for c, features in PHONEME_FEATURE_DICT.items() if c in CONSONANT_SET
})

PHONEME_FEATURE_DICT.update({
    f'{c}ʼ': {'place': features['place'], 'manner': features['manner'], 'voiced': features['voiced'], 'labialized': features['labialized'], 'aspirated': False, 'ejective': True}
    for c, features in PHONEME_FEATURE_DICT.items() if c in CONSONANT_SET
})

PHONEME_FEATURE_DICT.update({
    f'{c}ʷ': {'place': features['place'], 'manner': features['manner'], 'voiced': features['voiced'], 'labialized': True, 'aspirated': features['aspirated'], 'ejective': features['ejective']}
    for c, features in PHONEME_FEATURE_DICT.items() if c in CONSONANT_SET
})

PHONEME_FEATURE_DICT.update({
    f'{v}̃': {'height': features['height'], 'backness': features['backness'], 'rounded': features['rounded'], 'nasalized': True, 'long': features['long']}
    for v, features in PHONEME_FEATURE_DICT.items() if v in VOWEL_SET
})

PHONEME_FEATURE_DICT.update({
    f'{v}ː': {'height': features['height'], 'backness': features['backness'], 'rounded': features['rounded'], 'nasalized': features['nasalized'], 'long': True}
    for v, features in PHONEME_FEATURE_DICT.items() if v in VOWEL_SET
})
