import sys
from pathlib import Path

from src.parsers import parse_config_file, parse_glosses
from src.vocabulary import generate_random_vocabulary
from src.random_preset import random_preset


def generate_vocabulary(config_path: Path, glosses_path: Path) -> None:
    """
    Generate a random vocabulary and save it to a file.
    """
    with open(config_path, 'r') as f:
        phonemes, patterns, stress = parse_config_file(f)

    if glosses_path is not None:
        with open(glosses_path, 'r') as f:
            glosses = parse_glosses(f)
    else:
        glosses = []

    vocabulary = generate_random_vocabulary(phonemes, patterns, stress, glosses)

    output_txt_path = Path(f'vocabulary_{config_path.stem}.txt')
    output_csv_path = Path(f'vocabulary_{config_path.stem}.csv')

    with output_txt_path.open('w') as f:
        for gloss, word in vocabulary.items():
            f.write(f'{word}: {gloss}\n')
    
    with output_csv_path.open('w') as f:
        for gloss, word in vocabulary.items():
            f.write(f'{word},{gloss}\n')

    print(f"Vocabulary generated and saved to {output_txt_path} and {output_csv_path}")


def generate_from_random_preset(glosses_path: Path) -> None:
    """
    Generate a random vocabulary from a random preset and save it to a file.
    """
    preset = random_preset()
    phonemes = preset['phonemes']
    patterns = preset['patterns']
    stress = preset['stress']

    if glosses_path is not None:
        with open(glosses_path, 'r') as f:
            glosses = parse_glosses(f)
    else:
        glosses = []

    vocabulary = generate_random_vocabulary(phonemes, patterns, stress, glosses)

    output_txt_path = Path(f'vocabulary_random.txt')
    output_csv_path = Path(f'vocabulary_random.csv')

    with output_txt_path.open('w') as f:
        for gloss, word in vocabulary.items():
            f.write(f'{word}: {gloss}\n')
    
    with output_csv_path.open('w') as f:
        for gloss, word in vocabulary.items():
            f.write(f'{word},{gloss}\n')

    print(f"Vocabulary generated and saved to {output_txt_path} and {output_csv_path}")

def main():
    if len(sys.argv) < 2:
        # second arg is config_file or the word "random"
        print("Usage: python generate.py <config_file | random> [<glosses_file>]")

        sys.exit(1)

    if len(sys.argv) > 2:
        glosses_path = Path(sys.argv[2])
    else:
        glosses_path = None

    if sys.argv[1] == "random":
        generate_from_random_preset(glosses_path)

    else:
        config_path = Path(sys.argv[1])
        generate_vocabulary(config_path, glosses_path)


if __name__ == '__main__':
    main()
