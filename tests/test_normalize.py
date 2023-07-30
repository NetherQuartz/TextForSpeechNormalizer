"""Tests for the package"""

import tsnorm

from tsnorm import CustomDictionary, WordForm, WordFormTags, Lemma, LemmaPOS


def test_stress():
    normalizer = tsnorm.Normalizer(stress_mark="+", stress_mark_pos="before")
    stressed_text = normalizer("Волки, ежи и хомяки. Вот они, обитатели леса.")
    assert stressed_text == "В+олки, еж+и и хомяк+и. Вот он+и, обит+атели л+еса."


def test_stress_yo():
    normalizer = tsnorm.Normalizer(stress_mark="+", stress_mark_pos="before", stress_yo=True)
    stressed_text = normalizer("Как хорошо-то, ёмана!")
    assert stressed_text == "Как хорош+о-то, +ёмана!"


def test_stress_monosyllabic():
    normalizer = tsnorm.Normalizer(stress_mark="+", stress_mark_pos="before", stress_monosyllabic=True)
    stressed_text = normalizer("Как хорошо, как привольно!")
    assert stressed_text == "К+ак хорош+о, к+ак прив+ольно!"


def test_min_word_len():
    normalizer = tsnorm.Normalizer(stress_mark="+", stress_mark_pos="before", stress_monosyllabic=True, min_word_len=2)
    stressed_text = normalizer("Как хорошо и не привольно!")
    assert stressed_text == "К+ак хорош+о и н+е прив+ольно!"

    normalizer.min_word_len = 3
    stressed_text = normalizer("Как хорошо и не привольно!")
    assert stressed_text == "К+ак хорош+о и не прив+ольно!"


def test_stress_mark_position():
    normalizer = tsnorm.Normalizer(stress_mark="-", stress_mark_pos="after")
    stressed_text = normalizer("Трупы оживали, землю разрывали")
    assert stressed_text == "Тру-пы ожива-ли, зе-млю разрыва-ли"

    normalizer = tsnorm.Normalizer(stress_mark="+", stress_mark_pos="before")
    stressed_text = normalizer("Трупы оживали, землю разрывали")
    assert stressed_text == "Тр+упы ожив+али, з+емлю разрыв+али"


def test_custom_dictionary():
    normalizer = tsnorm.Normalizer(stress_mark="+", stress_mark_pos="before")
    stressed_text = normalizer("Мы приехали из Редании")
    assert stressed_text == "Мы при+ехали из Редании"

    dictionary = CustomDictionary(
        word_forms=[
            WordForm("Редании", 3, WordFormTags(singular=True, genitive=True), "Редания")
        ],
        lemmas=[
            Lemma("Редания", LemmaPOS(NOUN=True))
        ]
    )

    normalizer.update_dictionary(dictionary)
    stressed_text = normalizer("Мы приехали из Редании")
    assert stressed_text == "Мы при+ехали из Ред+ании"

    normalizer = tsnorm.Normalizer(stress_mark="+", stress_mark_pos="before", custom_dictionary=dictionary)
    stressed_text = normalizer("Мы приехали из Редании")
    assert stressed_text == "Мы при+ехали из Ред+ании"
