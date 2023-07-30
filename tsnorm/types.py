"""Types for tsnorm"""

from dataclasses import dataclass


@dataclass
class WordFormTags:

    plural: bool = False
    singular: bool = False
    nominative: bool = False
    genitive: bool = False
    dative: bool = False
    accusative: bool = False
    instrumental: bool = False
    prepositional: bool = False
    locative: bool = False
    present: bool = False
    past: bool = False
    future: bool = False


@dataclass
class LemmaPOS:

    ADJ: bool = False
    ADP: bool = False
    ADV: bool = False
    AFFIX: bool = False
    CCONJ: bool = False
    CHARACTER: bool = False
    COMBINING_FORM: bool = False
    DET: bool = False
    INTERFIX: bool = False
    INTJ: bool = False
    NOUN: bool = False
    NUM: bool = False
    PARTICLE: bool = False
    PHRASE: bool = False
    PNOUN: bool = False
    PREFIX: bool = False
    PREP_PHRASE: bool = False
    PRON: bool = False
    PROVERB: bool = False
    PUNCT: bool = False
    SUFFIX: bool = False
    SYMBOL: bool = False
    VERB: bool = False


@dataclass
class WordForm:

    word_form: str
    stress_pos: int | list[int]
    form_tags: WordFormTags
    lemma: str


@dataclass
class Lemma:

    lemma: str
    lemma_tags: LemmaPOS


def tags_to_list(tags: WordFormTags | LemmaPOS) -> list[str]:
    """Transform dataclass into list of strings"""

    dict_tags = tags.__dict__
    output = []

    for key, value in dict_tags.items():
        if value:
            output.append(key)

    return output


class CustomDictionary:
    """Class of a custom dictionary to extend normalizer dictionary"""

    word_forms: dict[str, list[dict[str, str | list[int]]]]
    lemmas: dict[str, dict[str, list[str]]]

    def __init__(self, word_forms: list[WordForm], lemmas: list[Lemma]) -> None:

        self.word_forms = {}

        for word_form in word_forms:

            word_form_dict = {
                "word_form": word_form.word_form,
                "stress_pos": [s_pos] if isinstance(s_pos := word_form.stress_pos, int) else s_pos,
                "form_tags": " ".join(tags_to_list(word_form.form_tags)),
                "lemma": word_form.lemma
            }

            current_wf = self.word_forms.get(word_form.word_form, [])
            current_wf.append(word_form_dict)
            self.word_forms[word_form.word_form] = current_wf

        self.lemmas = {}

        for lemma in lemmas:

            lemma_dict = {
                "pos": tags_to_list(lemma.lemma_tags),
                "rank": 0
            }

            self.lemmas[lemma.lemma] = lemma_dict
