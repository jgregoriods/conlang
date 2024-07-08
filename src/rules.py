RULES = {
    'opening': {
        'rules' : {
            'pʰ': 'f',
            'tʰ': 's',
            'kʰ': 'x',
            'p': 'f',
            't': 's',
            'k': 'x',
            'f': 'h',
            's': 'h',
            'x': 'h',
            'h': ''
            },
        },
    'sonorization': {
        'rules' : {
            'p': 'b',
            't': 'd',
            'k': 'g',
            'b': 'v',
            'd': 'z',
            'g': 'ɣ',
            'v': 'w',
            'z': 'ɹ',
            'ɣ': 'j',
            'w': '',
            'ɹ': '',
            'j': ''
            },
        },
    'grimms_law': {
        'rules' : {
            'p': 'f',
            't': 'θ',
            'k': 'x',
            'b': 'p',
            'd': 't',
            'g': 'k',
            'bʰ': 'b',
            'dʰ': 'd',
            'gʰ': 'g'
            },
        },
    'great_vowel_shift': {
        'rules' : {
            'iː': 'aj',
            'eː': 'iː',
            'ɛː': 'ej',
            'aː': 'ej',
            'uː': 'aw',
            'oː': 'uː',
            'ɔː': 'ow'
            },
        },
    'palatalization_velar': {
        'rules' : {
            'k I': 'tʃ I',
            'g I': 'dʒ I',
            'x I': 'ç I',
            'ɣ I': 'ʝ I'
            },
        'wildcards': {
            'I': ['i', 'e', 'eː', 'iː', 'ɛ', 'ɪ', 'ɛː', 'j', 'ɪː']
            }
        },
    'palatalization_alveolar': {
        'rules' : {
            't I': 'tʃ I',
            'd I': 'dʒ I',
            's I': 'ʃ I',
            'z I': 'ʒ I',
            'n I': 'ɲ I',
            'l I': 'ʎ I'
            },
        'wildcards': {
            'I': ['i', 'e', 'eː', 'iː', 'ɛ', 'ɪ', 'ɛː', 'j', 'ɪː']
            }
        },
    'palatalization_back': {
        'rules': {
            'k A': 'tʃ A'
        },
        'wildcards': {
            'A': ['a', 'ɑ', 'ɒ', 'ɔ', 'ɔː', 'ɒː', 'ɑː', 'ɒː', 'ɔː', 'ɔ', 'ɒ', 'ɑ']
        }
    },
    'canaanite_shift': {
        'rules' : {
            'aː': 'oː',
            },
        },
    'yiddish_breaking': {
        'rules' : {
            'ɛː': 'ɛj',
            'oː': 'ɔj',
            'øː': 'ɛj',
            'iː': 'aj',
            'yː': 'aj',
            'uː': 'ɔj'
            },
        'condition': 'stressed'
        },
    'romance_breaking': {
        'rules' : {
            'e': 'je',
            'o': 'wo',
            'ɛ': 'jɛ',
            'ɔ': 'wɔ'
            },
        'condition': 'stressed'
        },
    'articulation_weakening': {
        'rules' : {
            'i': 'e',
            'u': 'o',
            'a': 'ə',
            'ɨ': 'ɘ',
            'y': 'ø',
            'ʉ': 'ɵ',
            },
        'condition': 'unstressed'
        },
    'inventory_reduction': {
        'rules' : {
            'ɛ': 'e',
            'ɔ': 'o',
            'ɪ': 'i',
            'ʊ': 'u',
            'ʌ': 'a',
            'ɒ': 'o',
            'ɜ': 'e',
            'ə': 'a',
            'y': 'i',
            'ø': 'e',
            'ɤ': 'o',
            'œ': 'e',
            'ɞ': 'o',
            'ɘ': 'e',
            'ɵ': 'o',
            'ɐ': 'a',
            'ɑ': 'a',
            },
        },
    'devoicing': {
        'rules' : {
            'b': 'p',
            'd': 't',
            'g': 'k',
            'v': 'f',
            'z': 's',
            'ɣ': 'x',
            'ʒ': 'ʃ',
            'ʝ': 'ç',
            'dʒ': 'tʃ',
            'bʰ': 'pʰ',
            'dʰ': 'tʰ',
            'gʰ': 'kʰ',
            'dz': 'ts'
            },
        },
    'fortition': {
        'rules' : {
            'j': 'dʒ',
            'θ': 't',
            'ð': 'd',
            'f': 'p',
            'v': 'b',
            'r': 'd',
            'l': 'd',
            'ɣ': 'g'
            },
        },
    'affrication': {
        'rules' : {
            'p': 'f',
            't': 's',
            'k': 'x'
            },
        },
    'gaelic_breaking': {
        'rules' : {
            'eː': 'iə',
            'oː': 'uə',
            },
        },
}

RULES['inventory_reduction']['rules'].update({
    k + 'ː': v for k, v in RULES['inventory_reduction']['rules'].items()
})

