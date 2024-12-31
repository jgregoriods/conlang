import sys
from pathlib import Path

from src.parsers import parse_vocabulary, parse_mutation_rules
from src.mutation import mutate_vocabulary


def mutate_vocabulary_file(vocabulary_path: Path, rules_path: Path, output_path: Path) -> None:
    """
    Apply mutation rules to an existing vocabulary and save the result.
    """
    with open(vocabulary_path, 'r') as f:
        vocabulary = parse_vocabulary(f)
    with open(rules_path, 'r') as f:
        rules = parse_mutation_rules(f)

    mutated_vocabulary = mutate_vocabulary(vocabulary, rules)

    with output_path.open('w') as f:
        for gloss, word in mutated_vocabulary.items():
            f.write(f'{gloss}: {word}\n')
    print(f"Mutated vocabulary saved to {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python mutate.py <vocabulary_path> <rules_path>")
        sys.exit(1)

    vocabulary_path = Path(sys.argv[2])
    rules_path = Path(sys.argv[3])
    output_path = Path(f'mutated_{vocabulary_path.stem}.txt')
    mutate_vocabulary_file(vocabulary_path, rules_path, output_path)


if __name__ == '__main__':
    main()
