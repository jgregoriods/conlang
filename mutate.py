import sys
from pathlib import Path

from src.parsers import parse_vocabulary, parse_mutation_rules
from src.mutation import mutate_vocabulary


def mutate_vocabulary_file(vocabulary_path: Path, rules_path: Path) -> None:
    """
    Apply mutation rules to an existing vocabulary and save the result.
    """
    with open(vocabulary_path, 'r') as f:
        vocabulary = parse_vocabulary(f)
    with open(rules_path, 'r') as f:
        rules = parse_mutation_rules(f)

    mutated_vocabulary = mutate_vocabulary(vocabulary, rules)

    output_txt_path = Path(f'mutated_{vocabulary_path.stem}.txt')
    output_csv_path = Path(f'mutated_{vocabulary_path.stem}.csv')

    with output_txt_path.open('w') as f:
        for gloss, word in mutated_vocabulary.items():
            f.write(f'{word}: {gloss}\n')
    
    with output_csv_path.open('w') as f:
        f.write('word,gloss\n')
        for gloss, word in mutated_vocabulary.items():
            f.write(f'{word},{gloss}\n')

    print(f"Mutated vocabulary saved to {output_txt_path} and {output_csv_path}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python mutate.py <vocabulary_file> <rules_file>")
        sys.exit(1)

    vocabulary_path = Path(sys.argv[1])
    rules_path = Path(sys.argv[2])

    mutate_vocabulary_file(vocabulary_path, rules_path)


if __name__ == '__main__':
    main()
