import numpy as np
from .phonemes import (
    CONSONANT_SEED, VOWEL_SEED, 
    CONSONANT_DICT, VOWEL_DICT, 
    PATTERNS, STRESS, LIQUIDS, FINALS
)

def random_preset():
    consonant_seed = CONSONANT_SEED[np.random.randint(len(CONSONANT_SEED))]
    vowel_seed = VOWEL_SEED[np.random.randint(len(VOWEL_SEED))]
    stress = STRESS[np.random.randint(len(STRESS))]
    
    # Initialize phoneme dictionary
    phonemes = {
        'C': consonant_seed.copy(),
        'V': vowel_seed.copy()
    }

    # Extend consonants with additional features
    features = ['voiced', 'aspirated', 'nasal', 'fricative']
    for feature in features:
        if np.random.rand() < 0.5:
            phonemes['C'].extend(CONSONANT_DICT[c][feature] for c in consonant_seed)
    
    # Add liquids and sibilants conditionally
    if np.random.rand() < 0.5:
        phonemes['C'].extend(LIQUIDS[np.random.randint(len(LIQUIDS))])
    if np.random.rand() < 0.5:
        phonemes['C'].append('s')

    # Extend vowels with long forms
    if np.random.rand() < 0.5:
        phonemes['V'].extend(VOWEL_DICT[v]['long'] for v in vowel_seed)

    # Add finals conditionally
    if np.random.rand() < 0.5:
        phonemes['F'] = FINALS[np.random.randint(len(FINALS))]

    # Ensure unique phonemes in each category
    phonemes = {k: list(set(v)) for k, v in phonemes.items()}

    # Randomly select patterns and extend with finals if applicable
    patterns = np.random.choice(
        PATTERNS, size=np.random.randint(1, len(PATTERNS) + 1), replace=False
    ).tolist()
    
    if 'F' in phonemes:
        if np.random.rand() < 0.5:
            patterns.extend(f"{p}F" for p in patterns if p.endswith('C'))
        else:
            patterns = [f"{p}F" for p in patterns if p.endswith('V')]

    return phonemes, patterns, stress
