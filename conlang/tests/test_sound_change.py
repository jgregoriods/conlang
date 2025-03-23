import pytest
from conlang.loader import load_vocabulary_data, load_sound_change_data


egyptian = load_vocabulary_data('Egyptian')
coptic = load_vocabulary_data('Coptic')
sound_change = load_sound_change_data('Egyptian')

egyptian_mutation = sound_change.apply_to_vocabulary(egyptian.vocabulary)


@pytest.mark.parametrize("original, mutated, target", zip(egyptian.vocabulary, egyptian_mutation, coptic.vocabulary))
def test_sound_change(original, mutated, target):
    """
    Test if the sound change results in the expected mutated words.
    """
    assert mutated == target
