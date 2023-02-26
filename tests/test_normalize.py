"""Tests for the package"""

import tsnorm


def test_stress():
    normalizer = tsnorm.Normalizer(stress_mark="+", stress_mark_pos="before")
    stressed_text = normalizer("Волки, ежики и хомяки. Вот они, обитатели леса.")
    assert stressed_text == "В+олки, +ёжики и хомяк+и. Вот он+и, обит+атели л+еса."
