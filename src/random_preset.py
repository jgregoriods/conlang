import numpy as np


PRESETS = {
    'polynesian': {
        'phonemes': {
            'C': ['m', 'n', 'ŋ', 'p', 't', 'k', 'h', 'r'],
            'V': ['a', 'e', 'i', 'o', 'u']
        },
        'patterns': ['CVCV', 'CVV', 'VCV'],
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
    },
    'pacific_coast': {
        'phonemes': {
            'C': ['t', 'ts', 'tɬ', 'k', 'kʷ', 'q', 'qʷ', 'ʔ',
                  'tʼ', 'tsʼ', 'tɬʼ', 'kʼ', 'kʷʼ', 'qʼ', 'qʷʼ',
                  's', 'ɬ', 'x', 'xʷ', 'χ', 'χʷ', 'h',
                  'm', 'n', 'l', 'j', 'w'],
            'V': ['i', 'iː', 'e', 'eː', 'a', 'aː', 'u', 'uː', 'ə']
        },
        'patterns': ['CVC'],
        'stress': [-1]
    },
    'uralic': {
        'phonemes': {
            'C': ['p', 't', 'tɕ', 'tʃ', 'k',
                  'm', 'n', 'ɲ', 'ŋ',
                  's', 'ɕ', 'ʃ',
                  'l', 'ʎ', 'r', 'j', 'w'],
            'Q': ['pt', 'ps', 'tk', 'tɕk', 'tʃk', 'kt', 'ktɕ', 'ktʃ', 'ks',
                  'mp', 'mt', 'mk', 'nt', 'ŋk',
                  'lk', 'lm', 'lw', 'rk', 'rm', 'rw'],
            'V': ['i', 'y', 'u', 'e', 'o', 'ɛ', 'a'],
            'F': ['a', 'i']
        },
        'patterns': ['CVCF', 'VCF'],
        'stress': [-2]
    },
    'germanic': {
        'phonemes': {
            'C': ['m', 'n',
                  'p', 'b', 't', 'd', 'k',
                  'f', 'θ', 's', 'z', 'ɣ',
                  'l', 'r', 'j', 'w'],
            'Q': ['pl', 'kl', 'fl', 'sl', 'bl',
                  'pr', 'tr', 'kr', 'fr', 'θr', 'br', 'dr',
                  'tw', 'dw', 'kw', 'θw', 'xw', 'sw',
                  'kn', 'sm', 'sn', 'sp', 'st', 'sk'],
            'F': ['ft', 'xt', 'fs', 'xs', 'zd',
                  'mp', 'ms', 'mb', 'nt', 'nk', 'ns', 'nd',
                  'lp', 'lt', 'lk', 'lf', 'ls', 'lb', 'lm', 'rp', 'rt', 'rk', 'rf', 'rs', 'rb',
                  'sp', 'st', 'sk'],
            'V': ['i', 'e', 'a', 'u'],
            'L': ['iː', 'eː', 'aː', 'uː', 'ɔː'],
            'D': ['aw', 'aj', 'ew', 'iw', 'ɔːw', 'ɔːj']
        },
        'patterns': ['CVC', 'QVC', 'CVF',
                     'CLC', 'QLC', 'CLF',
                     'CDC', 'QDC',
                     'VC', 'VF', 'DC',
                     'LC', 'LF'],
        'stress': [-2]
    },
    'caucasus': {
        'phonemes': {
            'C': ['m', 'n',
                  'pʼ', 'tʼ', 'tsʼ', 'tʃʼ', 'kʼ', 'qʼ',
                  'b', 'd', 'dz', 'dʒ', 'g', 'gʷ',
                  's', 'ʃ', 'χ', 'χʷ', 'ħ', 'ħʷ',
                  'z', 'ʒ', 'ʁ', 'ʁʷ',
                  'l', 'r'],
            'V': ['a', 'ə'],
        },
        'patterns': ['CVC', 'CV', 'VC', 'CVCV', 'VCV'],
        'stress': [-2]
    },
    'bantu': {
        'phonemes': {
            'C': ['m', 'n', 'ɲ',
                  'p', 't', 'tʃ', 'k',
                  'b', 'd', 'dʒ', 'g'],
            'Q': ['mp', 'mb', 'nt', 'nd', 'ŋk', 'ŋg', 'ntʃ', 'ndʒ'],
            'V': ['i', 'e', 'a', 'o', 'u']
        },
        'patterns': ['CVCV', 'CVQV', 'QVCV',
                     'CV', 'QV', 'VCV', 'VQV'],
        'stress': [-1, -2]
    }
}


def random_preset():
    # return PRESETS[np.random.choice(list(PRESETS.keys()))]
    return PRESETS['bantu']
