import sys
from pathlib import Path

from src.parsers import parse_file, parse_glosses
from src.vocabulary import generate_random_vocabulary


def generate_vocabulary(config_path: Path, glosses_path: Path, output_path: Path) -> None:
    """
    Generate a random vocabulary and save it to a file.
    """
    with open(config_path, 'r') as f:
        phonemes, patterns, stress = parse_file(f)

    if glosses_path is not None:
        with open(glosses_path, 'r') as f:
            glosses = parse_glosses(f)
    else:
        glosses = []

    vocabulary = generate_random_vocabulary(phonemes, patterns, stress, glosses)

    with output_path.open('w') as f:
        for gloss, word in vocabulary.items():
            f.write(f'{gloss}: {word}\n')
    print(f"Vocabulary generated and saved to {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate.py <config_file> <glosses_file>")
        sys.exit(1)

    config_path = Path(sys.argv[2])

    if len(sys.argv) > 3:
        glosses_path = Path(sys.argv[3])
    else:
        glosses_path = None

    output_path = Path(f'vocabulary_{config_path.stem}.txt')
    generate_vocabulary(config_path, glosses_path, output_path)


if __name__ == '__main__':
    main()
