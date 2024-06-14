# Rules for sound change
RULES = {
    'opening_1': {
        'rules' : {
            'p': 'ɸ',
            't': 'θ',
            'k': 'x',
            'ɸ': 'h',
            'θ': 'h',
            'x': 'h',
            'h': ''
        },
    },
    'opening_2': {
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
    'sonorization_1': {
        'rules' : {
            'p': 'b',
            't': 'd',
            'k': 'g',
            'b': 'β',
            'd': 'ð',
            'g': 'ɣ',
            'β': 'w',
            'ð': 'ɹ',
            'ɣ': 'j',
            'w': '',
            'ɹ': '',
            'j': ''
        },
    },
    'sonorization_2': {
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
            'i:': 'aɪ',
            'e:': 'i:',
            'ɛ:': 'eɪ',
            'a:': 'eɪ',
            'u:': 'aʊ',
            'o:': 'u:',
            'ɔ:': 'oʊ'
        },
    },
    'palatalization_1': {
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
    'palatalization_2': {
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
            'ɛ:': 'ɛɪ',
            'o:': 'ɔɪ',
            'ø:': 'ɛɪ',
            'i:': 'aɪ',
            'y:': 'aɪ',
            'u:': 'ɔɪ'
        },
    },
    'romance_breaking': {
        'rules' : {
            'e': 'je',
            'o': 'wo',
            'ɛ': 'jɛ',
            'ɔ': 'wɔ'
        },
    },
}
