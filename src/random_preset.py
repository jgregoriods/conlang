import numpy as np


PRESETS = {
    'minimalist': {
        'phonemes': {
            'C': ['m', 'n', 'p', 't', 'k', 'h', 'r'],
            'V': ['a', 'e', 'i', 'o', 'u']
        },
        'patterns': ['CVCV', 'VCV'],
        'stress': [-2]
    },
    'semitic': {
        'phonemes': {
            'C': ['m', 'n', 't', 'k', 'q', 'ʔ', 'b', 'd', 'g', 'f', 's', 'ʃ', 'χ',
                  'h', 'ħ', 'z', 'ʕ', 'j', 'w', 'r', 'l'],
            'V': ['a', 'i', 'u'],
            'L': ['aː', 'iː', 'uː']
        },
        'patterns': ['CVC', 'CLC', 'CVCV', 'CLCV', 'CVCVC', 'CLCVC'],
        'stress': [-2]
    },
    'sinitic': {
        'phonemes': {
            'C': ['m', 'n', 'ɲ', 'ŋ',
                  'p', 't', 'ts', 'tʃ', 'k',
                  'pʰ', 'tʰ', 'tsʰ', 'tʃʰ', 'kʰ',
                  'b', 'd', 'dz', 'dʒ', 'g',
                  's', 'z', 'ʃ', 'ʒ',
                  'ʔ', 'x', 'ɣ', 'l'
                  ],
            'V': ['i', 'u', 'a', 'e', 'o'],
            'G': ['j', 'w'],
            'F': ['m', 'n', 'ŋ', 'p', 't', 'k', 'w', 'j']
        },
        'patterns': ['CV', 'CGV', 'CVF', 'CGVF'],
        'stress': [-1]
    },
    'amazonian':
    {
        'phonemes': {
            'C': ['m', 'n', 'ɲ',
                  'p', 't', 'k', 'ʔ',
                  'w', 'j', 'r',
                  'ʃ', 'h'],
            'V': ['i', 'e', 'a', 'o', 'u',
                  'ɛ', 'ɔ', 'ɯ']
        },
        'patterns': ['CVCV', 'VCV'],
        'stress': [-1]
    },
    'andean': {
        'phonemes': {
            'C': ['m', 'n', 'ɲ',
                  'p', 't', 'tʃ', 'k', 'q', 's',
                  'w', 'j', 'r', 'l', 'ʎ', 'h'],
            'V': ['a', 'i', 'u'],
            'Q': ['rm', 'rp', 'rk', 'rq',
                  'sp', 'sk', 'sq', 'sm',
                  'kp', 'kt', 'ks',
                  'qp', 'qt', 'qs'],
            'F': ['n', 's', 'k', 'r']
        },
        'patterns': ['CVCV', 'VCV', 'CVQV', 'VQV',
                     'CVCVF', 'VCVF', 'CVQVF', 'VQVF'],
        'stress': [-2]
    },
    'nilotic': {
        'phonemes': {
            'C': ['m', 'n', 'ŋ', 'ɲ',
                  'p', 't', 'c', 'k',
                  'b', 'd', 'ɟ', 'g',
                  's',
                  'r', 'l', 'j', 'w'],
            'G': ['j', 'w'],
            'V': ['i', 'e', 'a', 'o', 'u',
                  'ɛ', 'ɔ', 'ʌ'],
        },
        'patterns': ['CVC', 'CGVC'],
        'stress': [-1]
    }
}


def random_preset():
    return PRESETS[np.random.choice(list(PRESETS.keys()))]
