# Conlang

![PyPI](https://img.shields.io/pypi/v/conlang)
![PyPI - Downloads](https://img.shields.io/pypi/dm/conlang)

Conlang is a Python library for creating and manipulating constructed languages.

## Installation

To install Conlang, run the following command:

```bash
pip install conlang
```

## Usage

Here is an example of how you can use Conlang to create and mutate a simple language:

```python
from conlang import Language, LanguageConfig, SoundChange

config = LanguageConfig.from_txt("config.txt")
language = Language("MyLanguage", config)
language.generate_vocabulary()

sound_change = SoundChange.from_txt("sound_change.txt")
mutated_vocabulary = sound_change.apply(language.vocabulary)
```

## Documentation

For more information on how to use Conlang, please refer to the [documentation](https://jgregoriods.github.io/conlang/).

## Contributing

If you would like to contribute to Conlang, please read the [contributing guidelines](CONTRIBUTING.md).

## License

Conlang is distributed under the terms of the [GNU General Public License v3.0](LICENSE).
