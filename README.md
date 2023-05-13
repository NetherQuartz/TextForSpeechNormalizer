# Automatic accentuation for Russian texts

Accentuation is a common task in speech-related fields, e.g., text-to-speech, speech recognition, or just language learning. This library puts stress marks in text using data from Wiktionary and syntactic analysis of Spacy.

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

## Acknowledgement

This library is based on code by @einhornus from his [article](https://habr.com/ru/articles/575100/) on Habr.
