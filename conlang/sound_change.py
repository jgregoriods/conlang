import numpy as np
import re

from .utils import split_phonemes, map_stress
from .vocabulary import Vocabulary
from .rules import RULES


class SoundChange:
    def __init__(self, rules: dict, wildcards: dict = None):
        self.rules = rules
        self.wildcards = wildcards

    def apply_to_word(self, word: str) -> str:
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
                prv, nxt = (
                    environment[:-1], None) if environment[-1] == '_' else (None, environment[1:])

            if prv:
                prev_idx = index - \
                    1 if index > 0 and phonemes[index -
                                                1] != "ˈ" else index - 2
                if prev_idx < 0 or (prv.islower() and phonemes[prev_idx] != prv) or (prv.isupper() and phonemes[prev_idx] not in self.wildcards[prv]):
                    return False

            if nxt:
                next_idx = index + \
                    1 if index < len(
                        phonemes) - 1 and phonemes[index + 1] != "ˈ" else index + 2
                if next_idx >= len(phonemes) or (nxt.islower() and phonemes[next_idx] != nxt) or (nxt.isupper() and phonemes[next_idx] not in self.wildcards[nxt]):
                    return False

            return True

        for i, phoneme in enumerate(phonemes):
            if phoneme in self.rules:
                for rule in self.rules[phoneme]:
                    after, environment = rule
                    if ('[+stress]' in environment and not stressed[i]) or ('[-stress]' in environment and stressed[i]):
                        continue
                    environment = environment.replace(
                        '[+stress]', '').replace('[-stress]', '').strip()
                    if matches_environment(i, environment):
                        res.append(after)
                        break
                else:
                    res.append(phoneme)
            else:
                res.append(phoneme)

        return re.sub('[∅0]', '', ''.join(res))

    def apply_to_vocabulary(self, vocabulary: Vocabulary) -> Vocabulary:
        mutated_vocabulary = Vocabulary()
        for word, gloss in vocabulary:
            mutated_word = self.apply_to_word(word)
            mutated_vocabulary.add_item(mutated_word, gloss)
        return mutated_vocabulary

    @staticmethod
    def from_txt(filename: str) -> 'SoundChange':
        rules = {}
        wildcards = {}

        with open(filename, 'r') as f:
            for line in f:
                if '>' in line:
                    line = line.split('>')
                    before = line[0].strip()
                    after = line[1].strip()
                    if before not in rules:
                        rules[before] = []
                    if '/' in after:
                        after, environment = after.split('/')
                        rules[before].append(
                            (after.strip(), environment.strip()))
                    else:
                        rules[before].append((after, ''))
                elif ':' in line:
                    line = line.split(':')
                    wildcard = line[0].strip()
                    phonemes = line[1].strip().split()
                    wildcards[wildcard] = phonemes

        return SoundChange(rules, wildcards)

    @staticmethod
    def random() -> 'SoundChange':
        rule_names = np.random.choice(
            list(RULES), size=np.random.randint(1, 6), replace=False)

        rules = {}
        wildcards = {}

        for rule_name in rule_names:
            for k, v in RULES[rule_name]['rules'].items():
                if k not in rules:
                    rules[k] = v
            wildcards.update(RULES[rule_name]['wildcards'])

        return SoundChange(rules, wildcards)
