from typing import TextIO


def parse_file(f: TextIO) -> list:
    """
    Parses the file line by line.
    """
    phonemes = {}
    patterns = []
    stress = []

    for line in f:
        if ':' in line:
            line = line.split(':')
            phonemes[line[0]] = line[1].strip().split()
        elif '-' in line:
            stress.extend(line.strip().split())
        elif line.isupper():
            patterns.extend(line.strip().split())

    stress = [int(s) for s in stress]

    return phonemes, patterns, stress


def parse_glosses(f: TextIO) -> list:
    """
    Parses the glosses from the given file.
    """
    glosses = []
    for line in f:
        glosses.append(line.strip())
    return glosses


def parse_mutation_rules(f: TextIO) -> dict:
    """
    Parses the mutation rules from the given file.
    """
    rules = {
        'rules': {},
        'wildcards': {}
    }
    for line in f:
        if '>' in line:
            line = line.split('>')
            before = line[0].strip()
            after = line[1].strip()
            if before not in rules['rules']:
                rules['rules'][before] = []
            if '/' in after:
                after, environment = after.split('/')
                rules['rules'][before].append((after.strip(), environment.strip()))
            else:
                rules['rules'][before].append((after, ''))
        elif ':' in line:
            line = line.split(':')
            wildcard = line[0].strip()
            phonemes = line[1].strip().split()
            rules['wildcards'][wildcard] = phonemes
    return rules


def parse_vocabulary(f: TextIO) -> dict:
    """
    Parses the vocabulary from the given file.
    """
    vocabulary = {}
    for line in f:
        line = line.split(':')
        gloss = line[0].strip()
        word = line[1].strip()
        vocabulary[gloss] = word
    return vocabulary
