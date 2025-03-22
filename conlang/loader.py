import importlib.resources

from .vocabulary import Vocabulary
from .language import Language
from .sound_change import SoundChangePipeline


def load_vocabulary_data(language_name: str) -> Language:
    if language_name not in ['Egyptian', 'Coptic']:
        raise ValueError(f'Language {language_name} not supported')
    text_file = importlib.resources.files('conlang.resources').joinpath(f'{language_name.lower()}.txt')
    vocabulary = Vocabulary.from_txt(text_file)
    language = Language.from_vocabulary('Egyptian', vocabulary)
    return language


def load_sound_change_data(language_name: str) -> str:
    if language_name != 'Egyptian':
        raise ValueError(f'Language {language_name} not supported')
    text_file = importlib.resources.files('conlang.resources').joinpath(f'{language_name.lower()}_sound_change.txt')
    sound_change = SoundChangePipeline.from_txt(text_file)
    return sound_change
