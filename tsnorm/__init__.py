from .normalize import Normalizer
from .types import CustomDictionary, WordForm, WordFormTags, Lemma, LemmaPOS

from .spacy_model import download_model

__version__ = "1.1.2"


download_model()
