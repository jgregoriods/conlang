import re


LENITION = {
    'p': 'f',
    't': 'θ',
    'k': 'x'
}


class SoundChange:
    def __init__(self):
        pass

    def apply(self, rules, word):
        regex = re.compile('|'.join(map(re.escape, rules)))
        return regex.sub(lambda match: rules[match.group(0)], word)

