RULES = {
    'opening': {
        'rules' : {
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
            'i:': 'aj',
            'e:': 'i:',
            'ɛ:': 'ej',
            'a:': 'ej',
            'u:': 'aw',
            'o:': 'u:',
            'ɔ:': 'ow'
            },
        },
    'palatalization_back': {
        'rules' : {
            'k I': 'tʃ I',
            'g I': 'dʒ I',
            'x I': 'ç I',
            'ɣ I': 'ʝ I',
            'j I': 'ʝ I',
            },
        'wildcards': {
            'I': ['i', 'e', 'e:', 'i:', 'ɛ', 'ɪ', 'ɛ:', 'j', 'ɪ:']
            }
        },
    'palatalization_front': {
        'rules' : {
            't I': 'tʃ I',
            'd I': 'dʒ I',
            's I': 'ʃ I',
            'z I': 'ʒ I',
            'n I': 'ɲ I',
            'l I': 'ʎ I'
            },
        'wildcards': {
            'I': ['i', 'e', 'e:', 'i:', 'ɛ', 'ɪ', 'ɛ:', 'j', 'ɪ:']
            }
        },
    'canaanite_shift': {
        'rules' : {
            'a:': 'o:',
            },
        },
    'yiddish_breaking': {
        'rules' : {
            'ɛ:': 'ɛj',
            'o:': 'ɔj',
            'ø:': 'ɛj',
            'i:': 'aj',
            'y:': 'aj',
            'u:': 'ɔj'
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
}

RULES['inventory_reduction']['rules'].update({
    k + ':': v for k, v in RULES['inventory_reduction']['rules'].items()
})

