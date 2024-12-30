import sys
from pathlib import Path

from src.parsers import (
    parse_phonemes,
    parse_patterns,
    parse_stress,
    parse_glosses,
    parse_vocabulary,
    parse_mutation_rules,
)
from src.vocabulary import generate_random_vocabulary
from src.mutation import mutate_vocabulary


def generate_vocabulary(folder: Path, glosses_path: Path, output_path: Path) -> None:
    """
    Generate a random vocabulary and save it to a file.
    """
    phonemes = parse_phonemes(folder / 'phonemes.txt')
    patterns = parse_patterns(folder / 'patterns.txt')
    stress = parse_stress(folder / 'stress.txt')
    glosses = parse_glosses(glosses_path)

    vocabulary = generate_random_vocabulary(phonemes, patterns, stress, glosses)

    with output_path.open('w') as f:
        for gloss, word in vocabulary.items():
            f.write(f'{gloss}: {word}\n')
    print(f"Vocabulary generated and saved to {output_path}")


def mutate_vocabulary_file(vocabulary_path: Path, rules_path: Path, output_path: Path) -> None:
    """
    Apply mutation rules to an existing vocabulary and save the result.
    """
    vocabulary = parse_vocabulary(vocabulary_path)
    rules = parse_mutation_rules(rules_path)

    mutated_vocabulary = mutate_vocabulary(vocabulary, rules)

    with output_path.open('w') as f:
        for gloss, word in mutated_vocabulary.items():
            f.write(f'{gloss}: {word}\n')
    print(f"Mutated vocabulary saved to {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <option> <args>")
        sys.exit(1)

    option = sys.argv[1]

    if option == 'generate':
        if len(sys.argv) < 3:
            print("Usage: python main.py generate <folder>")
            sys.exit(1)

        folder = Path(sys.argv[2])
        glosses_path = Path('swadesh.txt')
        output_path = Path('vocabulary.txt')
        generate_vocabulary(folder, glosses_path, output_path)

    elif option == 'mutate':
        if len(sys.argv) < 4:
            print("Usage: python main.py mutate <vocabulary_path> <rules_path>")
            sys.exit(1)

        vocabulary_path = Path(sys.argv[2])
        rules_path = Path(sys.argv[3])
        output_path = Path('mutated_vocabulary.txt')
        mutate_vocabulary_file(vocabulary_path, rules_path, output_path)

    else:
        print(f"Unknown option: {option}")
        print("Valid options are: 'generate', 'mutate'")
        sys.exit(1)


if __name__ == '__main__':
    main()
