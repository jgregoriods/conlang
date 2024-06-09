OPENING1 = ({
    'p': 'ɸ',
    't': 'θ',
    'k': 'x',
    'ɸ': 'h',
    'θ': 'h',
    'x': 'h',
    'h': ''
}, None)

OPENING2 = ({
    'p': 'f',
    't': 's',
    'k': 'x',
    'f': 'h',
    's': 'h',
    'x': 'h',
    'h': ''
}, None)

SONORIZATION = {
    'p': 'b',
    't': 'd',
    'k': 'g',
    'ɣ': 'j',
    'w': '',
    'ɹ': '',
    'j': ''
}

SONORIZATION1 = ({
    'b': 'β',
    'd': 'ð',
    'g': 'ɣ',
    'β': 'w',
    'ð': 'ɹ'
}, None)
SONORIZATION1[0].update(SONORIZATION)

SONORIZATION2 = ({
    'b': 'v',
    'd': 'z',
    'g': 'ɣ',
    'v': 'w',
    'z': 'ɹ'
}, None)
SONORIZATION2[0].update(SONORIZATION)

GRIMMS_LAW = ({
    'p': 'f',
    't': 'θ',
    'k': 'x',
    'b': 'p',
    'd': 't',
    'g': 'k',
    'bʰ': 'b',
    'dʰ': 'd',
    'gʰ': 'g'
}, None)

GREAT_VOWEL_SHIFT = ({
    'i:': 'aɪ',
    'e:': 'i:',
    'ɛ:': 'eɪ',
    'a:': 'eɪ',
    'u:': 'aʊ',
    'o:': 'u:',
    'ɔ:': 'oʊ'
}, 'stressed')

PALATALIZATION1 = ({
    'k': 'tʃ',
    'g': 'dʒ',
    'x': 'ç',
    'ɣ': 'ʝ',
    'j': 'ʝ'
}, {'next': ['i']})

PALATALIZATION2 = ({
    't': 'tʃ',
    'd': 'dʒ',
    's': 'ʃ',
    'z': 'ʒ',
    'n': 'ɲ',
    'l': 'ʎ'
}, {'next': ['i']})
