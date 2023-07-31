# Automatic accentuation for texts in Russian

Accentuation is a common task in such speech-related fields as text-to-speech, speech recognition and language learning. This library is used to mark stressed vowels in given texts using the data from Wiktionary and syntactic analysis of [Spacy](https://github.com/explosion/spaCy).

### Installation
Python 3.10 and above supported.
```bash
pip install tsnorm
```

### General usage
```Python
from tsnorm import Normalizer


normalizer = Normalizer(stress_mark=chr(0x301), stress_mark_pos="after")
normalizer("Словно куклой в час ночной теперь он может управлять тобой")

# Output: Сло́вно ку́клой в час ночно́й тепе́рь он мо́жет управля́ть тобо́й
```

### Change stress mark and its position
```Python
normalizer = Normalizer(stress_mark="+", stress_mark_pos="before")
normalizer("Трупы оживали, землю разрывали")

# Output: Тр+упы ожив+али, з+емлю разрыв+али
```

### Stress yo (Ё)
```Python
normalizer = Normalizer(stress_mark="+", stress_mark_pos="before", stress_yo=True)
normalizer("Погаснет день, луна проснётся, и снова зверь во мне очнётся")

# Output: Пог+аснет день, лун+а просн+ётся, и сн+ова зверь во мне очн+ётся
```

### Stress monosyllabic words
```Python
normalizer = Normalizer(stress_mark="+", stress_mark_pos="before", stress_monosyllabic=True)
normalizer("Панки грязи не боятся, кто устал — ушёл сдаваться!")

# Output: П+анки гр+язи н+е бо+ятся, кт+о уст+ал — ушёл сдав+аться!
```

### Change minimum length of words to be stressed
```Python
normalizer = Normalizer(stress_mark="+", stress_mark_pos="before", stress_monosyllabic=True)
normalizer("Разбежавшись, прыгну со скалы, вот я был и вот меня не стало")

# Output: Разбеж+авшись, пр+ыгну с+о скал+ы, в+от +я б+ыл +и в+от мен+я н+е ст+ало


normalizer = Normalizer(stress_mark="+", stress_mark_pos="before", stress_monosyllabic=True, min_word_len=2)
normalizer("Разбежавшись, прыгну со скалы, вот я был и вот меня не стало")

# Output: Разбеж+авшись, пр+ыгну с+о скал+ы, в+от я б+ыл и в+от мен+я н+е ст+ало


normalizer = Normalizer(stress_mark="+", stress_mark_pos="before", stress_monosyllabic=True, min_word_len=3)
normalizer("Разбежавшись, прыгну со скалы, вот я был и вот меня не стало")

# Output: Разбеж+авшись, пр+ыгну со скал+ы, в+от я б+ыл и в+от мен+я не ст+ало
```

### Expand normalizer dictionary

```Python
from tsnorm import Normalizer, CustomDictionary, WordForm, Lemma, WordFormTags, LemmaPOS


normalizer = Normalizer("+", "before")

normalizer("Охотник Себастьян, что спал на чердаке")
# Output: Ох+отник Себастьян, что спал на чердак+е

dictionary = CustomDictionary(
    word_forms=[
        WordForm("Себастьян", 7, WordFormTags(singular=True, nominative=True), "Себастьян")
    ],
    lemmas=[
        Lemma("Себастьян", LemmaPOS(PNOUN=True))
    ]
)

normalizer.update_dictionary(dictionary)

normalizer("Охотник Себастьян, что спал на чердаке")
# Output: Ох+отник Себасть+ян, что спал на чердак+е
```

It's also possible to pass `CustomDictionary` at normalizer initialization:
```Python
normalizer = Normalizer("+", "before", custom_dictionary=dictionary)
```

To add your custom words to normalizer dictionary you must pass two lists to `CustomDictionary`:
1. a list of `WordForm` objects, which are forms of each word with case, tense and lemma information, as well as the positions of stressed letters,
2. a list of `Lemma` objects, which are records of lemmas with their parts of speech.

Parts of speech for lemmas are configured using the `LemmaPOS` class which stores [universal POS tags](https://universaldependencies.org/u/pos/).

## Acknowledgement

This library is based on code by @einhornus from his [article](https://habr.com/ru/articles/575100/) on Habr.
