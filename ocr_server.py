# 1. Настройки
IMAGE_PATH = input('Введите путь к файлу')  # Путь к вашему PNG-файлу
OUTPUT_TXT = "output.txt"  # Файл для сохранения результата
LANGUAGES = ["ru", "en"]  # Языки распознавания

# 2. Инициализация EasyOCR
reader = easyocr.Reader(LANGUAGES)

# 3. Распознавание текста
result = reader.readtext(IMAGE_PATH, detail=0,paragraph = True)
text = " ".join(result)  # Объединяем строки через перенос

# 4. Сохранение в файл
with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
    f.write(text)

print(f"Текст успешно сохранён в файл: {OUTPUT_TXT}")
print("Распознанный текст:")
print(text)
