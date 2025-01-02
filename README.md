# Conlang Vocabulary Generator and Mutator

This project provides tools to generate a random vocabulary from phonemes, word patterns, and stress rules, and to mutate existing vocabularies based on specified mutation rules.

## Usage

### Generating Vocabulary

```
python generate.py <config_file> [<glosses_file>]
```

To generate a vocabulary, you need to provide a configuration file in txt format. The configuration file should contain the following information:

- Phonemes: sets of phonemes (or consonant clusters) identified by uppercase labels, separated by spaces, with each set separated by a newline.
```
C: p t k m n ŋ s ʃ h l j w
Q: pr tr kr
N: m n ŋ
V: a e i o u
```

- Word Patterns: combinations of phoneme sets identified by their labels, separated by spaces or newlines.
```
CVCV VCV CVN CVCVN QVCV
```

- Stress Rules: negative integers indicating possible stressed syllables, separated by spaces or newlines. -1 stands for the final syllable, -2 for the penultimate syllable, etc.
```
-1 -2
```

Optionally, you can provide a glosses file in txt format. The glosses file should contain a list of glosses separated by newlines. If not provided, the vocabulary will be generated from the Swadesh 200-word list.

The resulting vocabulary will be saved in both txt and csv files with the same name as the configuration file.

### Mutating Vocabulary

```
python mutate.py <vocabulary_file> <rules_file>
```

To mutate a vocabulary, you need to provide a vocabulary file in txt or csv format. If in txt format, the vocabulary file should contain a list of items separated by newlines, with each item consisting of a word followed by its gloss, separated by a colon or a tab. For example:
```
ˈsan: brother
ˈsaːnat: sister
```

If in csv format, the file should contain two columns, with the first column containing the words and the second column containing the glosses.

You also need to provide a rules file in txt format. The rules file should contain a list of mutation rules separated by newlines. The following example shows the format of mutation rules:

```
p > b
t > d
k > tʃ / _i
k > g / _a
r > 0 / _#
```

In this example, `p` becomes `b`and `t` becomes `d` unconditionally, while `k` becomes `tʃ` before `i` and `g` before `a`, and `r` is deleted at the end of a word (you can use both `0` and `∅` to represent deletion).

You can also use wildcards, defining them in the same way as the phoneme sets in the configuration file:
```
p > b / V_V
V: a e i o u
```
