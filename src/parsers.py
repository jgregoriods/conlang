def parse_phonemes(phonemes_path: str) -> dict:
    """
    Parses the phonemes from the given file path.
    """
    phonemes = {}
    with open(phonemes_path, 'r') as f:
        for line in f:
            line = line.split(':')
            phonemes[line[0]] = line[1].strip().split()
    return phonemes


def parse_patterns(patterns_path: str) -> list:
    """
    Parses the patterns from the given file path.
    """
    patterns = []
    with open(patterns_path, 'r') as f:
        for line in f:
            patterns.extend(line.strip().split())
    return patterns


def parse_stress(stress_path: str) -> list:
    """
    Parses the stress from the given file path.
    """
    stress = []
    with open(stress_path, 'r') as f:
        for line in f:
            stress.extend(line.strip().split())
    return [int(s) for s in stress]


def parse_glosses(glosses_path: str) -> list:
    """
    Parses the glosses from the given file path.
    """
    glosses = []
    with open(glosses_path, 'r') as f:
        for line in f:
            glosses.append(line.strip())
    return glosses


def parse_mutation_rules(rules_path: str) -> dict:
    """
    Parses the mutation rules from the given file path.
    """
    rules = {
        'rules': {},
        'wildcards': {}
    }
    with open(rules_path, 'r') as f:
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


def parse_vocabulary(vocabulary_path: str) -> dict:
    """
    Parses the vocabulary from the given file path.
    """
    vocabulary = {}
    with open(vocabulary_path, 'r') as f:
        for line in f:
            line = line.split(':')
            gloss = line[0].strip()
            word = line[1].strip()
            vocabulary[gloss] = word
    return vocabulary
