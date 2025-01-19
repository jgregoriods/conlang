from .phonemes import VOWELS, CONSONANTS


RULES = {
    'opening': {
        'rules': {
            'pʰ': [('p', '')],
            'tʰ': [('t', '')],
            'tsʰ': [('ts', '')],
            'cʰ': [('c', '')],
            'tʃʰ': [('tʃ', '')],
            'kʰ': [('k', '')],
            'qʰ': [('q', '')],
            'p': [('f', '')],
            't': [('s', '')],
            'ts': [('s', '')],
            'c': [('ç', '')],
            'tʃ': [('ʃ', '')],
            'k': [('x', '')],
            'q': [('χ', '')],
            'f': [('h', '')],
            's': [('h', '')],
            'ç': [('h', '')],
            'ʃ': [('h', '')],
            'x': [('h', '')],
            'χ': [('h', '')],
            'h': [('0', '')],
        },
        'wildcards': {}
    },
    'sonorization': {
        'rules': {
            'p': [('b', '')],
            't': [('d', '')],
            'c': [('ɟ', '')],
            'ts': [('dz', '')],
            'tʃ': [('dʒ', '')],
            'k': [('g', '')],
            'q': [('ɢ', '')],
            'b': [('v', '')],
            'd': [('ð', '')],
            'g': [('ɣ', '')],
            'dz': [('z', '')],
            'dʒ': [('ʒ', '')],
            'ɢ': [('ʁ', '')],
            'v': [('w', '')],
            'z': [('j', '')],
            'ð': [('j', '')],
            'ɣ': [('j', '')],
            'ʒ': [('j', '')],
            'w': [('0', '')],
            'j': [('0', '')],
        },
        'wildcards': {}
    },
    'sonorization_intervocalic': {
        'rules': {
            'p': [('b', 'V_V')],
            't': [('d', 'V_V')],
            'c': [('ɟ', 'V_V')],
            'ts': [('dz', 'V_V')],
            'tʃ': [('dʒ', 'V_V')],
            'k': [('g', 'V_V')],
            'q': [('ɢ', 'V_V')],
            'b': [('v', 'V_V')],
            'd': [('ð', 'V_V')],
            'g': [('ɣ', 'V_V')],
            'dz': [('z', 'V_V')],
            'dʒ': [('ʒ', 'V_V')],
            'ɢ': [('ʁ', 'V_V')],
            'v': [('w', 'V_V')],
            'z': [('j', 'V_V')],
            'ð': [('j', 'V_V')],
            'ɣ': [('j', 'V_V')],
            'ʒ': [('j', 'V_V')],
            'w': [('0', 'V_V')],
            'j': [('0', 'V_V')],
        },
        'wildcards': {
            'V': VOWELS
        }
    },
    'palatalization_velar': {
        'rules': {
            'k': [('tʃ', '_I')],
            'g': [('dʒ', '_I')],
            'x': [('ʃ', '_I')],
            'ɣ': [('ʒ', '_I')],
        },
        'wildcards': {
            'I': ['i', 'e', 'ɛ', 'ɨ', 'iː', 'eː', 'ɛː', 'ɨː', 'j']
        }
    },
    'palatalization_alveolar': {
        'rules': {
            's': [('ʃ', '_I')],
            'z': [('ʒ', '_I')],
            't': [('tʃ', '_I')],
            'd': [('dʒ', '_I')],
        },
        'wildcards': {
            'I': ['i', 'e', 'ɛ', 'ɨ', 'iː', 'eː', 'ɛː', 'ɨː', 'j']
        }
    },
    'romance_breaking': {
        'rules': {
            'e': [('je', '[+stress]')],
            'ɛ': [('je', '[+stress]')],
            'o': [('wo', '[+stress]')],
            'ɔ': [('wo', '[+stress]')],
        },
        'wildcards': {}
    },
    'great_vowel_shift': {
        'rules': {
            'iː': [('aj', '[+stress]')],
            'eː': [('iː', '[+stress]')],
            'aː': [('eː', '[+stress]')],
            'oː': [('uː', '[+stress]')],
            'uː': [('aw', '[+stress]')],
        },
        'wildcards': {}
    },
    'elision': {
        'rules': {},
        'wildcards': {}
    },
    'vowel_reduction': {
        'rules': {},
        'wildcards': {}
    },
    'final_consonant_loss': {
        'rules': {},
        'wildcards': {}
    },
    'final_vowel_loss': {
        'rules': {},
        'wildcards': {}
    },
    'yiddish_breaking': {
        'rules': {
            'eː': [('ej', '[+stress]')],
            'oː': [('oj', '[+stress]')],
            'ɛː': [('ej', '[+stress]')],
            'øː': [('ej', '[+stress]')],
            'iː': [('aj', '[+stress]')],
            'uː': [('oj', '[+stress]')],
            'yː': [('aj', '[+stress]')],
        },
        'wildcards': {}
    },
    'devoicing': {
        'rules': {
            'b': [('p', '')],
            'd': [('t', '')],
            'ɟ': [('c', '')],
            'ɡ': [('k', '')],
            'ɢ': [('q', '')],
            'v': [('f', '')],
            'ð': [('θ', '')],
            'ɣ': [('x', '')],
            'ʒ': [('ʃ', '')],
            'z': [('s', '')],
            'dʒ': [('tʃ', '')],
            'dz': [('ts', '')],
            'ʁ': [('χ', '')]
        },
        'wildcards': {}
    },
    'fortition': {
        'rules': {
            'j': [('dʒ', '')],
            'θ': [('t', '')],
            'ð': [('d', '')],
            'f': [('p', '')],
            'v': [('b', '')],
            'ɣ': [('g', '')],
            'r': [('d', '')],
            'l': [('d', '')],
        },
        'wildcards': {}
    }
}

RULES['elision']['rules'] = {k: [('0', '[-stress]')] for k in VOWELS}
RULES['vowel_reduction']['rules'] = {k: [('ə', '[-stress]')] for k in VOWELS}
RULES['final_consonant_loss']['rules'] = {k: [('0', '_#')] for k in CONSONANTS}
RULES['final_vowel_loss']['rules'] = {k: [('0', '_# [-stress]')] for k in VOWELS}
