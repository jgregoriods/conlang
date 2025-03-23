Installation
------------

To install the package, run the following command:

.. code-block:: bash

    pip install conlang

Usage
-----

Generating a conlang
~~~~~~~~~~~~~~~~~~~~

To generate a conlang, you need to provide a configuration object. The
simplest way to do this is to load a text file containing the configuration
data. For example:

.. code-block:: text

    C: p t k m n ŋ s ʃ h l j w
    Q: pr tr kr
    N: m n ŋ
    V: a e i o u

    CVCV VCV CVN CVCVN QVCV

    -1 -2

As you can see, you must define sets of phonemes (or clusters) identified by
uppercase letters; a list of syllable structures; and a list of stressed
syllable positions (as negative indices).

To generate the configuration object from this file, you can use the
:func:`conlang.LanguageConfig.from_txt` function:

.. code-block:: python

    from conlang import LanguageConfig

    config = LanguageConfig.from_txt('path/to/config.txt')

Alternatively, you can generate a random configuration object, which will
choose from a set of predefined values meant to resemble natural languages:

.. code-block:: python

    from conlang import LanguageConfig

    config = LanguageConfig.random()

Instead of choosing randomly, you can also select a specific preset:

.. code-block:: python

    from conlang import LanguageConfig

    config = LanguageConfig.load_preset('germanic')

Once you have the configuration object, you can generate a conlang object
and its associated lexicon:

.. code-block:: python

    from conlang import Conlang

    conlang = Conlang('Name', config)
    conlang.generate_vocabulary()

This will generate a vocabulary from the 200-word Swadesh list. You can
specify a different list by passing it as an argument to the method:

.. code-block:: python

    glosses = [...]
    conlang.generate_vocabulary(glosses)

Loading a vocabulary
~~~~~~~~~~~~~~~~~~~~

If you have a vocabulary file, you can load it directly to generate
a vocabulary object using the :func:`conlang.Vocabulary.from_txt` method:

.. code-block:: python

    from conlang import Vocabulary

    vocabulary = Vocabulary.from_txt('path/to/vocabulary.txt')

The vocabulary text file should contain words and their glosses separated by
a colon or another delimiter (to be specified as an argument to the method):

.. code-block:: text

    ˈsan: brother
    ˈsaːnat: sister
    ˈnaːcar: god
    naˈcaːrat: goddess

If you already have a vocabulary object, a configuration object or even a
language object can be generated from it. The configuration will be detected
from the vocabulary:

.. code-block:: python

    conlang = Conlang.from_vocabulary('Name', vocabulary)

Mutating a vocabulary
~~~~~~~~~~~~~~~~~~~~~

You can mutate a vocabulary object by applying a set of rules to it. You must
create a SoundChange object, which can be loaded from a text file:

.. code-block:: text

    p > b
    k > tʃ / _i
    k > g / _a
    r > 0 / _#

This file contains a set of sound changes, each on a separate line. The
syntax is `source > target / context`, where the context is optional.
In this example, `p` becomes `b` unconditionally, while `k` becomes `tʃ`
before `i` and `g` before `a`, and `r` is deleted at the end of a word.

In addition to the phoneme environment, you can specify stress:

.. code-block:: text

    a > ɔ / [+stress]
    a > ə / [-stress]
    t > 0 / _# [-stress]

You can also use wildcards:

.. code-block:: text

    k > tʃ / _I
    p > b / V_V

    I: i iː j

Notice that if you use the symbol `V` you don't need to specify that it
refers to all vowels.

You are not restricted to single phonemes, but can use sequences:

.. code-block:: text

    Vt > ə / _# [-stress]
    Vw > 0 / _# [-stress]

Finally, it's possible to use feature-based rules. For example:

.. code-block:: text

    C [-voiced] > C [+voiced] / V_V

You can load the text file using the :func:`conlang.SoundChange.from_txt` method:

.. code-block:: python

    from conlang import SoundChange

    sound_change = SoundChange.from_txt('path/to/sound_change.txt')

You can also create a random sound change object, which will select from a
set of predefined, realistic sound changes:

.. code-block:: python

    from conlang import SoundChange

    sound_change = SoundChange.random()

As with the configuration object, you can load a specific sound change preset:

.. code-block:: python

    from conlang import SoundChange

    sound_change = SoundChange.load_preset('great_vowel_shift')

Once you have the sound change object, you can apply it to the vocabulary
object:

.. code-block:: python

    mutated_vocabulary = sound_change.apply_to_vocabulary(vocabulary)

This will return a new vocabulary object with the sound changes applied.

You can chain multiple sound changes together by using the :class:`conlang.SoundChangePipeline`:

.. code-block:: python

    from conlang import SoundChange, SoundChangePipeline

    sound_change1 = SoundChange.from_txt('path/to/sound_change1.txt')
    sound_change2 = SoundChange.from_txt('path/to/sound_change2.txt')
    ...

    pipeline = SoundChangePipeline([sound_change1, sound_change2, ...])
    mutated_vocabulary = pipeline.apply_to_vocabulary(vocabulary)

Alternatively, you can load a pipeline from a text file, which must contain
the sound change rules identified by labels between brackets:

.. code-block:: text

    (stage 1)
    p > b
    t > d

    (stage 2)
    a > ɔ / [+stress]
    a > ə / [-stress]

    (stage 3)
    k > tʃ / _i

.. code-block:: python

    from conlang import SoundChangePipeline

    pipeline = SoundChangePipeline.from_txt('path/to/pipeline.txt')
    mutated_vocabulary = pipeline.apply_to_vocabulary(vocabulary)

Saving a vocabulary
~~~~~~~~~~~~~~~~~~~

You can save a vocabulary object to a text or csv file using the :func:`conlang.Vocabulary.to_txt`
or :func:`conlang.Vocabulary.to_csv` methods:

.. code-block:: python

    vocabulary.to_txt('path/to/vocabulary.txt')
    vocabulary.to_csv('path/to/vocabulary.csv')
