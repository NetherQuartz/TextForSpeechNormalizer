from spacy.util import get_installed_models
from spacy.cli import download

MODEL = "ru_core_news_md"


def download_model() -> None:
    if MODEL not in get_installed_models():
        download(MODEL)
