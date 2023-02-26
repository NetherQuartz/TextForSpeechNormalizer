import pickle

import spacy

from pkg_resources import resource_stream
from typing import Any, Optional

from .spacy_model import MODEL


class Normalizer:

    stress_mark: str
    stress_mark_pos: str

    _model: spacy.language.Language
    _word_forms: dict[str, list[dict[str, Any]]]
    _lemmas: dict[str, dict[str, Any]]

    def __init__(self, stress_mark: str, stress_mark_pos: str) -> None:

        if stress_mark_pos not in ["before", "after"]:
            raise ValueError("stress_mark_pos must be one of ['before', 'after']")

        self.stress_mark = stress_mark
        self.stress_mark_pos = stress_mark_pos

        self._word_forms = pickle.load(resource_stream(__name__, "dictionary/wordforms.dat"))
        self._lemmas = pickle.load(resource_stream(__name__, "dictionary/lemmas.dat"))
        
        self._model = spacy.load(MODEL)

        for word, forms in self._word_forms.items():
            if " " in word or "-" in word:
                if len(forms) == 1:
                    self._model.tokenizer.add_special_case(word, [{"ORTH": word}])
                    self._model.tokenizer.add_special_case(word.capitalize(), [{"ORTH": word.capitalize()}])
    
    def put_stress_mark(self, word: str, stress_pos: list[int]) -> str:
        word = list(word)
        insert_num = 0
        for pos in stress_pos:
            pos += insert_num
            word.insert(pos, self.stress_mark)
            insert_num += len(self.stress_mark)

        return "".join(word)

    def derive_single_accentuation(self, interpretations: list[dict[str, Any]]) -> Optional[str]:
        if len(interpretations) == 0:
            return None

        res = self.put_stress_mark(interpretations[0]["word_form"], interpretations[0]["stress_pos"])
        for el in interpretations[1:]:
            if self.put_stress_mark(el["word_form"], el["stress_pos"]) != res:
                return None
        return res

    def compatible(self, interpretation: str, lemma: str, tag: str) -> bool:
        if lemma in self._lemmas:
            pos_exists = False
            possible_poses = self._lemmas[lemma]["pos"]
            for i in range(len(possible_poses)):
                if possible_poses[i] in tag:
                    pos_exists = True
                    break
            if not pos_exists:
                return False

        if interpretation == "canonical":
            return True
        if "plural" in interpretation and "Number=Plur" not in tag:
            return False
        if "singular" in interpretation and "Number=Sing" not in tag:
            return False
        if "nominative" not in interpretation and "Case=Nom" in tag:
            return False
        if "genitive" not in interpretation and "Case=Gen" in tag:
            return False
        if "dative" not in interpretation and "Case=Dat" in tag:
            return False

        if "accusative" not in interpretation and "Case=Acc" in tag:
            adj = False
            if "ADJ" in tag and "Animacy=Inan" in tag:
                adj = True
            if not adj:
                return False

        if "instrumental" not in interpretation and "Case=Ins" in tag:
            return False
        if "prepositional" not in interpretation and "locative" not in interpretation and "Case=Loc" in tag:
            return False
        if ("present" in interpretation or "future" in interpretation) and "Tense=Past" in tag:
            return False
        if ("past" in interpretation or "future" in interpretation) and "Tense=Pres" in tag:
            return False
        if ("past" in interpretation or "present" in interpretation) and "Tense=Fut" in tag:
            return False

        return True

    def tokenize(self, text: str) -> list[dict[str, Any]]:

        res = []
        for token in self._model(text):
            if token.pos_ != "PUNCT":
                word = { "token": token.text, "tag": token.tag_ }

                if word["token"] in self._word_forms:
                    word["interpretations"] = self._word_forms[word["token"]]

                if word["token"].lower() in self._word_forms:
                    word["interpretations"] = self._word_forms[word["token"].lower()]

                word["lemma"] = token.lemma_
                word["is_punctuation"] = False
                word["uppercase"] = word["token"].upper() == word["token"]
                word["starts_with_a_capital_letter"] = word["token"][0].upper() == word["token"][0]
            else:
                word = { "token": token.text, "is_punctuation": True }
            
            word["whitespace"] = token.whitespace_
            res.append(word)

        return res

    def accentuate_word(self, word: dict[str, Any]) -> str:
        if "tag" in word and "PROPN" in word["tag"]:
            return word["token"]

        if word["is_punctuation"] or "interpretations" not in word:
            return word["token"]
        else:
            if res := self.derive_single_accentuation(word["interpretations"]):
                return res
            else:
                compatible_interpretations = []
                for interp in word["interpretations"]:
                    if self.compatible(interp["form_tags"], interp["lemma"], word["tag"]):
                        compatible_interpretations.append(interp)

                if res := self.derive_single_accentuation(compatible_interpretations):
                    return res
                else:
                    new_compatible_interpretations = []
                    for interp in compatible_interpretations:
                        if interp["lemma"] == word["lemma"]:
                            new_compatible_interpretations.append(interp)

                    if res := self.derive_single_accentuation(new_compatible_interpretations):
                        return res
                    else:
                        return word["token"]

    def __call__(self, text: str) -> str:

        res = ""
        words = self.tokenize(text)
        for word in words:
            accentuated = self.accentuate_word(word)
            if "starts_with_a_capital_letter" in word and word["starts_with_a_capital_letter"]:
                accentuated = accentuated.capitalize()
            if "uppercase" in word and word["uppercase"]:
                accentuated = accentuated.upper()
            res += accentuated
            res += word["whitespace"]
            
        return res
