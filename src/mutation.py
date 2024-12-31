import re

from .utils import split_phonemes, map_stress


def mutate_word(word: str, rule_dict: dict) -> str:
    """
    Mutates the given word using the given rules.
    """
    phonemes = split_phonemes(word)
    stressed = map_stress(phonemes)

    res = []

    def matches_environment(index, environment):
        """
        Check if the phoneme matches the given environment.
        """
        if not environment:
            return True

        if environment == "#_":
            return index == 0
        if environment == "_#":
            return index == len(phonemes) - 1

        parts = environment.split('_')
        if len(parts) == 2:
            prv, nxt = parts
        else:
            prv, nxt = (environment[:-1], None) if environment[-1] == '_' else (None, environment[1:])

        if prv:
            prev_idx = index - 1 if index > 0 and phonemes[index - 1] != "ˈ" else index - 2
            if prev_idx < 0 or (prv.islower() and phonemes[prev_idx] != prv) or (prv.isupper() and phonemes[prev_idx] not in rule_dict['wildcards'][prv]):
                return False

        if nxt:
            next_idx = index + 1 if index < len(phonemes) - 1 and phonemes[index + 1] != "ˈ" else index + 2
            if next_idx >= len(phonemes) or (nxt.islower() and phonemes[next_idx] != nxt) or (nxt.isupper() and phonemes[next_idx] not in rule_dict['wildcards'][nxt]):
                return False

        return True

    for i, phoneme in enumerate(phonemes):
        rules = rule_dict['rules']
        if phoneme in rules:
            for rule in rules[phoneme]:
                after, environment = rule
                if ('[+stress]' in environment and not stressed[i]) or ('[-stress]' in environment and stressed[i]):
                    continue
                environment = environment.replace('[+stress]', '').replace('[-stress]', '').strip()
                if matches_environment(i, environment):
                    res.append(after)
                    break
            else:
                res.append(phoneme)
        else:
            res.append(phoneme)

    return re.sub('[∅0]', '', ''.join(res))


def mutate_vocabulary(vocabulary: dict, rule_dict: dict) -> dict:
    """
    Mutates the given vocabulary using the given rules.
    """
    mutated_vocabulary = {}
    for gloss, word in vocabulary.items():
        mutated_word = mutate_word(word, rule_dict)
        mutated_vocabulary[gloss] = mutated_word
    return mutated_vocabulary
