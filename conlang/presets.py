PRESETS = {
    'polynesian': {
        'phonemes': {
            'C': ['m', 'n', 'ŋ',
                  'p', 't', 'k',
                  'h',
                  'r'],
            'V': ['a', 'e', 'i', 'o', 'u']
        },
        'patterns': ['CVV', 'CVCV', 'VCV', 'VCVV'],
        'stress': [-2]
    },
    'semitic': {
        'phonemes': {
            'C': ['m', 'n',
                  't', 'k', 'q', 'ʔ',
                  'b', 'd', 'g',
                  'f', 's', 'ʃ', 'χ', 'h', 'ħ',
                  'z', 'ʕ',
                  'r', 'l',
                  'j', 'w'],
            'V': ['a', 'i', 'u'],
            'L': ['aː', 'iː', 'uː']
        },
        'patterns': ['CVC', 'CLC', 'CVCV', 'CLCV', 'CVCVC', 'CLCVC'],
        'stress': [-2]
    },
    'sinitic': {
        'phonemes': {
            'C': ['m', 'n', 'ɲ', 'ŋ',
                  'p', 't', 'ts', 'tʃ', 'k', 'ʔ',
                  'pʰ', 'tʰ', 'tsʰ', 'tʃʰ', 'kʰ',
                  'b', 'd', 'dz', 'dʒ', 'g',
                  's', 'ʃ', 'x',
                  'z', 'ʒ', 'ɣ',
                  'l'],
            'V': ['a', 'e', 'i', 'o', 'u'],
            'G': ['j', 'w'],
            'F': ['m', 'n', 'ŋ',
                  'p', 't', 'k',
                  'j', 'w']
        },
        'patterns': ['CV', 'CGV', 'CVF', 'CGVF'],
        'stress': [-1]
    },
    'amazonian':
    {
        'phonemes': {
            'C': ['m', 'n', 'ɲ',
                  'p', 't', 'k', 'ʔ',
                  'ʃ', 'h',
                  'r',
                  'j', 'w'],
            'V': ['a', 'e', 'i', 'o', 'u',
                  'ɛ', 'ɔ', 'ɯ']
        },
        'patterns': ['CV', 'VCV', 'CVCV'],
        'stress': [-1]
    },
    'andean': {
        'phonemes': {
            'C': ['m', 'n', 'ɲ',
                  'p', 't', 'tʃ', 'k', 'q',
                  's', 'h',
                  'r', 'l', 'ʎ',
                  'j', 'w'],
            'V': ['a', 'i', 'u'],
            'Q': ['rm', 'rp', 'rk', 'rq',
                  'sp', 'sk', 'sq', 'sm',
                  'kp', 'kt', 'ks',
                  'qp', 'qt', 'qs'],
            'F': ['n', 'k', 's', 'r']
        },
        'patterns': ['VCV', 'CVCV', 'VQV', 'CVQV', 'VCVF', 'CVCVF', 'VQVF', 'CVQVF'],
        'stress': [-2]
    },
    'nilotic': {
        'phonemes': {
            'C': ['m', 'n', 'ŋ', 'ɲ',
                  'p', 't', 'c', 'k',
                  'b', 'd', 'ɟ', 'g',
                  's',
                  'r', 'l',
                  'j', 'w'],
            'G': ['j', 'w'],
            'V': ['a', 'e', 'i', 'o', 'u',
                  'ɛ', 'ɔ', 'ʌ']
        },
        'patterns': ['CVC', 'CGVC'],
        'stress': [-1]
    },
    'pacific_coast': {
        'phonemes': {
            'C': ['m', 'n',
                  't', 'ts', 'tɬ', 'k', 'kʷ', 'q', 'qʷ', 'ʔ',
                  'tʼ', 'tsʼ', 'tɬʼ', 'kʼ', 'kʷʼ', 'qʼ', 'qʷʼ',
                  's', 'ɬ', 'x', 'xʷ', 'χ', 'χʷ', 'h',
                  'l',
                  'j', 'w'],
            'V': ['a', 'e', 'i', 'u',
                  'ə',
                  'aː', 'eː', 'iː', 'uː']
        },
        'patterns': ['CVC'],
        'stress': [-1]
    },
    'uralic': {
        'phonemes': {
            'C': ['m', 'n', 'ɲ', 'ŋ', 'p', 't', 'tɕ', 'tʃ', 'k', 's', 'ɕ', 'ʃ',
                  'r', 'l', 'ʎ', 'j', 'w'],
            'Q': ['pt', 'ps', 'tk', 'tɕk', 'tʃk', 'kt', 'ktɕ', 'ktʃ', 'ks',
                  'mp', 'mt', 'mk', 'nt', 'ŋk', 'lk', 'lm', 'lw', 'rk', 'rm',
                  'rw'],
            'V': ['a', 'e', 'i', 'o', 'u', 'y', 'ɛ'],
            'F': ['a', 'i']
        },
        'patterns': ['VCF', 'CVCF'],
        'stress': [-2]
    },
    'germanic': {
        'phonemes': {
            'C': ['m', 'n',
                  'p', 't', 'k',
                  'b', 'd',
                  'f', 'θ', 's', 'h',
                  'z',
                  'r', 'l',
                  'j', 'w'],
            'Q': ['pl', 'kl', 'bl', 'fl', 'sl',
                  'pr', 'tr', 'kr', 'br', 'dr', 'fr', 'θr',
                  'tw', 'kw', 'dw', 'θw', 'sw', 'hw',
                  'kn', 'sm', 'sn', 'sp', 'st', 'sk'],
            'F': ['mp', 'nt', 'nk', 'ns',
                  'zd',
                  'rt', 'rk', 'rs'],
            'V': ['a', 'e', 'i', 'u'],
            'L': ['aː', 'eː', 'iː', 'uː', 'ɔː'],
            'D': ['aw', 'aj','ew', 'iw']
        },
        'patterns': ['CVC', 'QVC', 'CVF',
                     'CLC', 'QLC',
                     'CDC', 'QDC',
                     'VC', 'VF', 'DC',
                     'LC'],
        'stress': [-2]
    },
    'caucasus': {
        'phonemes': {
            'C': ['m', 'n',
                  'pʼ', 'tʼ', 'tsʼ', 'tʃʼ', 'kʼ', 'qʼ',
                  'b', 'd', 'dz', 'dʒ', 'g', 'gʷ',
                  's', 'ʃ', 'χ', 'χʷ', 'ħ', 'ħʷ',
                  'z', 'ʒ', 'ʁ', 'ʁʷ',
                  'r', 'l'],
            'V': ['a', 'ə'],
        },
        'patterns': ['CV', 'VC', 'CVC', 'VCV', 'CVCV'],
        'stress': [-2]
    },
    'bantu': {
        'phonemes': {
            'C': ['m', 'n', 'ɲ',
                  'p', 't', 'tʃ', 'k',
                  'b', 'd', 'dʒ', 'g'],
            'Q': ['mp', 'mb', 'nt', 'nd', 'ŋk', 'ŋg', 'ntʃ', 'ndʒ'],
            'V': ['a', 'e', 'i', 'o', 'u']
        },
        'patterns': ['CV', 'QV', 'VCV', 'VQV',
                     'CVCV', 'CVQV', 'QVCV'],
        'stress': [-1, -2]
    },
    'maya': {
        'phonemes': {
            'C': ['m', 'n',
                  'p', 't', 'ts', 'tʃ', 'k', 'ʔ',
                  'b',
                  'pʼ', 'tʼ', 'tsʼ', 'tʃʼ', 'kʼ',
                  's', 'ʃ', 'χ', 'h',
                  'l',
                  'j', 'w'],
            'F': ['m', 'n',
                  'ts', 'tʃ', 'k', 'ʔ',
                  'b',
                  'tsʼ', 'tʃʼ', 'kʼ',
                  'ʃ', 'h',
                  'l'],
            'V': ['a', 'e', 'i', 'o', 'u',
                  'aː', 'eː', 'iː', 'oː', 'uː']
        },
        'patterns': ['CVF'],
        'stress': [-1]
    },
    'caddoan': {
        'phonemes': {
            'C': ['n',
                  'p', 't', 'tʃ', 'k', 'ʔ',
                  's', 'ʃ', 'x', 'h',
                  'r',
                  'w'],
            'F': ['t', 'k', 'ʔ'],
            'V': ['a', 'e', 'i', 'o', 'u',
                  'aː', 'eː', 'iː', 'oː', 'uː']
        },
        'patterns': ['CVCV', 'CVCVF'],
        'stress': [-1, -2]
    }
}
