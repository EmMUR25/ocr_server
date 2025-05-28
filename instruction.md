## Инструкция запуска и пример кода
Установка (одна команда):

pip install easyocr

pip install python = 3.12

Пример кода:
```python

import easyocr

reader = easyocr.Reader(['ru', 'en'])  # Инициализация для рус/англ
result = reader.readtext('image.png')  # Распознавание
for (bbox, text, confidence) in result:
    print(f"Текст: {text} (точность: {confidence:.2f})")
```
