import numpy as np

from .phonemes import (CONSONANT_SEED, VOWEL_SEED,
                       CONSONANT_DICT, VOWEL_DICT, PATTERNS, STRESS, LIQUIDS, FINALS)


def random_preset():
    consonant_seed = CONSONANT_SEED[np.random.randint(0, len(CONSONANT_SEED))]
    vowel_seed = VOWEL_SEED[np.random.randint(0, len(VOWEL_SEED))]
    stress = STRESS[np.random.randint(0, len(STRESS))]

    phonemes = {'C': consonant_seed.copy(),
                'V': vowel_seed.copy()}

    # voiced
    if np.random.rand() < 0.5:
        phonemes['C'].extend([CONSONANT_DICT[c]['voiced']
                              for c in consonant_seed])

    # aspirated
    if np.random.rand() < 0.5:
        phonemes['C'].extend([CONSONANT_DICT[c]['aspirated']
                              for c in consonant_seed])

    # nasal
    if np.random.rand() < 0.5:
        phonemes['C'].extend([CONSONANT_DICT[c]['nasal']
                             for c in consonant_seed])

    # fricative
    if np.random.rand() < 0.5:
        phonemes['C'].extend([CONSONANT_DICT[c]['fricative']
                              for c in consonant_seed])

    # liquids
    if np.random.rand() < 0.5:
        phonemes['C'].extend(LIQUIDS[np.random.randint(0, len(LIQUIDS))])

    # long vowels
    if np.random.rand() < 0.5:
        phonemes['V'].extend([VOWEL_DICT[v]['long'] for v in vowel_seed])

    # finals
    if np.random.rand() < 0.5:
        phonemes['F'] = [f for f in FINALS[np.random.randint(
            0, len(FINALS))] if f in phonemes['C']]
    
    phonemes = {k: list(set(v)) for k, v in phonemes.items()}

    # patterns
    patterns = np.random.choice(
        PATTERNS, np.random.randint(1, len(PATTERNS) + 1), replace=False).tolist()
    if 'F' in phonemes and phonemes['F']:
        patterns.extend([p + 'F' for p in patterns if p[-1] == 'V'])

    print(phonemes, patterns, stress)

    return phonemes, patterns, stress
