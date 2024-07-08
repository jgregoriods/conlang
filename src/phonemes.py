CONSONANTS = {
    'm': ['nasal', 'bilabial', 'sonorant'],
    'n': ['nasal', 'alveolar', 'sonorant'],
    'ɳ': ['nasal', 'retroflex', 'sonorant'],
    'ɲ': ['nasal', 'palatal', 'sonorant'],
    'ŋ': ['nasal', 'velar', 'sonorant'],
    'ɴ': ['nasal', 'uvular', 'sonorant'],
    'p': ['plosive', 'bilabial', 'voiceless'],
    'b': ['plosive', 'bilabial', 'voiced'],
    't': ['plosive', 'alveolar', 'voiceless'],
    'd': ['plosive', 'alveolar', 'voiced'],
    'ʈ': ['plosive', 'retroflex', 'voiceless'],
    'ɖ': ['plosive', 'retroflex', 'voiced'],
    'c': ['plosive', 'palatal', 'voiceless'],
    'ɟ': ['plosive', 'palatal', 'voiced'],
    'k': ['plosive', 'velar', 'voiceless'],
    'g': ['plosive', 'velar', 'voiced'],
    'q': ['plosive', 'uvular', 'voiceless'],
    'ɢ': ['plosive', 'uvular', 'voiced'],
    'ʔ': ['plosive', 'glottal', 'voiceless'],
    'ɸ': ['fricative', 'bilabial', 'voiceless'],
    'β': ['fricative', 'bilabial', 'voiced'],
    'f': ['fricative', 'labiodental', 'voiceless'],
    'v': ['fricative', 'labiodental', 'voiced'],
    'θ': ['fricative', 'dental', 'voiceless'],
    'ð': ['fricative', 'dental', 'voiced'],
    's': ['fricative', 'alveolar', 'voiceless'],
    'z': ['fricative', 'alveolar', 'voiced'],
    'ʃ': ['fricative', 'palato-alveolar', 'voiceless'],
    'ʒ': ['fricative', 'palato-alveolar', 'voiced'],
    'ʂ': ['fricative', 'retroflex', 'voiceless'],
    'ʐ': ['fricative', 'retroflex', 'voiced'],
    'ç': ['fricative', 'palatal', 'voiceless'],
    'ʝ': ['fricative', 'palatal', 'voiced'],
    'x': ['fricative', 'velar', 'voiceless'],
    'ɣ': ['fricative', 'velar', 'voiced'],
    'χ': ['fricative', 'uvular', 'voiceless'],
    'ʁ': ['fricative', 'uvular', 'voiced'],
    'ħ': ['fricative', 'pharyngeal', 'voiceless'],
    'ʕ': ['fricative', 'pharyngeal', 'voiced'],
    'h': ['fricative', 'glottal', 'voiceless'],
    'ɦ': ['fricative', 'glottal', 'voiced'],
    'ʋ': ['approximant', 'labiodental', 'voiced'],
    'ɹ': ['approximant', 'alveolar', 'voiced'],
    'ɻ': ['approximant', 'retroflex', 'voiced'],
    'j': ['approximant', 'palatal', 'voiced'],
    'ɰ': ['approximant', 'velar', 'voiced'],
    'ɾ': ['flap', 'alveolar', 'voiced'],
    'ɽ': ['flap', 'retroflex', 'voiced'],
    'r': ['trill', 'alveolar', 'voiced'],
    'ʀ': ['uvular', 'trill', 'voiced'],
    'ɬ': ['fricative', 'alveolar', 'lateral', 'voiceless'],
    'ɮ': ['fricative', 'alveolar', 'lateral', 'voiced'],
    'l': ['lateral', 'alveolar', 'voiced'],
    'ɭ': ['lateral', 'retroflex', 'voiced'],
    'ʎ': ['lateral', 'palatal', 'voiced'],
    'ʟ': ['lateral', 'velar', 'voiced'],
    'ts': ['affricate', 'alveolar', 'voiceless'],
    'dz': ['affricate', 'alveolar', 'voiced'],
    'tʃ': ['affricate', 'palato-alveolar', 'voiceless'],
    'dʒ': ['affricate', 'palato-alveolar', 'voiced'],
    'ʈʂ': ['affricate', 'retroflex', 'voiceless'],
    'ɖʐ': ['affricate', 'retroflex', 'voiced'],
    'tɬ': ['affricate', 'alveolar', 'lateral', 'voiceless'],
    'dɮ': ['affricate', 'alveolar', 'lateral', 'voiced'],
    'w': ['approximant', 'bilabial', 'voiced'],
}

ASPIRATED = {f'{k}ʰ':v + ['aspirated'] for k,v in CONSONANTS.items() if 'plosive' in v or 'affricate' in v}
EJECTIVE = {f'{k}ʼ':v + ['ejective'] for k,v in CONSONANTS.items() if ('plosive' in v or 'affricate' in v) and 'voiceless' in v}

CONSONANTS.update(ASPIRATED)
CONSONANTS.update(EJECTIVE)

VOWELS = {
    'i': ['close', 'front', 'unrounded'],
    'y': ['close', 'front', 'rounded'],
    'ɨ': ['close', 'central', 'unrounded'],
    'ʉ': ['close', 'central', 'rounded'],
    'e': ['close-mid', 'front', 'unrounded'],
    'ø': ['close-mid', 'front', 'rounded'],
    'ɘ': ['close-mid', 'central', 'unrounded'],
    'ɵ': ['close-mid', 'central', 'rounded'],
    'ə': ['mid', 'central', 'unrounded'],
    'ɯ': ['close', 'back', 'unrounded'],
    'u': ['close', 'back', 'rounded'],
    'ɤ': ['close-mid', 'back', 'unrounded'],
    'o': ['close-mid', 'back', 'rounded'],
    'ɛ': ['open-mid', 'front', 'unrounded'],
    'œ': ['open-mid', 'front', 'rounded'],
    'ɜ': ['open-mid', 'central', 'unrounded'],
    'ɞ': ['open-mid', 'central', 'rounded'],
    'ʌ': ['open-mid', 'back', 'unrounded'],
    'ɔ': ['open-mid', 'back', 'rounded'],
    'æ': ['near-open', 'front', 'unrounded'],
    'ɐ': ['near-open', 'central', 'unrounded'],
    'a': ['open', 'front', 'unrounded'],
    'ɶ': ['open', 'front', 'rounded'],
    'ɑ': ['open', 'back', 'unrounded'],
    'ɒ': ['open', 'back', 'rounded']
}

LONG_VOWELS = {f'{k}ː':v + ['long'] for k,v in VOWELS.items()}
NASAL_VOWELS = {f'{k}̃':v + ['nasal'] for k,v in VOWELS.items()}
NASAL_LONG_VOWELS = {f'{k}̃ː':v + ['nasal', 'long'] for k,v in VOWELS.items()}
VOWELS.update(LONG_VOWELS)
VOWELS.update(NASAL_VOWELS)
VOWELS.update(NASAL_LONG_VOWELS)

PHONEMES = {**CONSONANTS, **VOWELS}
SUPRASEGMENTALS = ["ˈ", "ː", "˩", "˧", "˥", "̃"]
SEMIVOWELS = ['j', 'ɰ', 'w']
