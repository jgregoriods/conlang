from src.language import Language
from src.sound_change import SoundChange
from numpy import random

from src.utils import split_syllables


def main():
    phonemes = {
        'V': ['a', 'i', 'e', 'u', 'o'],
        'C': ['p', 'k', 't', 's', 'm', 'n', 'l']
    }
    patterns = [
        ['C', 'V'],
        ['C', 'V', 'C', 'V'],
        ['V', 'C', 'V'],
        ['V', 'C', 'V', 'C', 'V']
    ]
    stress = [1]

    language = Language(phonemes, patterns, stress, 'agglutinative', 'SOV')
    language.generate_vocabulary()

    indices = random.choice(list(range(len(language.vocabulary.items))), 30, replace=False)
    words = [language.vocabulary.items[i]['word'] for i in indices]

    sound_change = SoundChange(random_rules=3)
    new_vocab = language.mutate(sound_change, 0.1)

    sc = SoundChange(random_rules=3)
    new_vocab_2 = language.mutate(sc, 0.1)

    new_words = [new_vocab.items[i]['word'] for i in indices]
    new_words_2 = [new_vocab_2.items[i]['word'] for i in indices]

    print('\n')
    for word, new_word, nw in zip(words, new_words, new_words_2):
        print(f"{word} -> {new_word}  {nw}")
    print('\n')


if __name__ == '__main__':
    main()
