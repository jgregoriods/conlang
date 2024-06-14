from src.language import Language
from src.sound_change import SoundChange
from src.rules import *
from numpy import random
from src.utils import split_syllables


def main():
    phonemes = {
        'V': ['a', 'i', 'u', 'a:', 'e', 'o'],
        'C': ['k', 'pʰ', 'tʰ', 'kʰ', 'b', 'd', 'g', 'm', 'n', 's', 'z', 'l', 'r']
    }
    patterns = [
        ['C', 'V', 'C', 'V'],
        ['V', 'C', 'V'],
        ['V', 'C', 'V', 'C', 'V'],
        ['C', 'V', 'C'],
        ['C', 'V', 'C', 'V', 'C']
    ]
    stress = [1, 2]

    language = Language(phonemes, patterns, stress, 'agglutinative', 'SOV')
    language.generate_vocabulary()

    indices = random.choice(list(range(len(language.vocabulary.items))), 5, replace=False)
    words = [language.vocabulary.items[i]['word'] for i in indices]
    print('\n')
    print(words)
    print('\n')

    pipeline = [
        RULES['palatalization_1'],
    ]

    sound_change = SoundChange(pipeline, 0.1)
    new_vocab = sound_change.evolve(language)

    new_words = [new_vocab.items[i]['word'] for i in indices]

    print(new_words)
    print('\n')


if __name__ == '__main__':
    main()
