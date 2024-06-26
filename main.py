from src.language import Language, parse_word, parse_vocabulary
from src.sound_change import SoundChange
from numpy import random
from src.vocabulary import Vocabulary

from src.utils import split_syllables, split_phonemes


LANGUAGE_TYPES = {
    'polynesian': {
        'phonemes': {
            'V': ['a', 'e', 'i', 'o', 'u'],
            'C': ['k', 't', 'r', 'h', 'm', 'p', 'ŋ', 'n', 'v']
        },
        'patterns': [
            'C V',
            'C V C V',
            'C V C V C V',
            'V C V',
        ],
        'stress': [-2],
        'word_order': 'VSO',
        'morphology': 'isolating'
    },
}


def main():

    vocab = Vocabulary.from_csv('sanskrit.csv')
    parsed = parse_vocabulary(vocab)
    language = Language(**parsed)
    language.generate_vocabulary()
    indices = random.choice(list(range(len(language.vocabulary.items))), 30, replace=False)
    words = [language.vocabulary.items[i] for i in indices]

    print('\n')
    for word in words:
        print(f"{word['word']} : {word['definition']}")
    print('\n')

    sound_change = SoundChange()
    new_vocab = language.mutate(sound_change, 0.2)

    sc = SoundChange()
    new_vocab_2 = language.mutate(sc, 0.2)

    new_words = [new_vocab.items[i]['word'] for i in indices]
    new_words_2 = [new_vocab_2.items[i]['word'] for i in indices]

    print('\n')
    for word, new_word, nw in zip(words, new_words, new_words_2):
        print(f"{word['word']} -> {new_word}  {nw}")
    print('\n')


if __name__ == '__main__':
    l = Language(**LANGUAGE_TYPES['polynesian'])
    l.generate_vocabulary()

    nl = l.mutate(SoundChange(random_rules=100), 0.0)

    random_indices = random.choice(list(range(len(l.vocabulary.items))), 20, replace=False)
    for i in random_indices:
        print(l.vocabulary.items[i]['word'], '->', nl.items[i]['word'])
