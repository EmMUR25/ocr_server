# language_manager.py
import easyocr

# Кэш для хранения инициализированных ридеров для разных наборов языков
# Ключ - кортеж языков (например, ('ru', 'en')), значение - объект Reader
reader_cache = {}

# Пример доступных языков (можно расширить на основе поддерживаемых EasyOCR)
# См. документацию EasyOCR для полного списка: https://www.jaided.ai/easyocr
SUPPORTED_LANGUAGES = {
    'abq': 'Abaza', 'ady': 'Adyghe', 'af': 'Afrikaans', 'ang': 'Angika', 'ar': 'Arabic',
    'as': 'Assamese', 'ava': 'Avar', 'az': 'Azerbaijani', 'be': 'Belarusian', 'bg': 'Bulgarian',
    'bh': 'Bihari', 'bho': 'Bhojpuri', 'bn': 'Bengali', 'bs': 'Bosnian', 'ca': 'Catalan',
    'ceb': 'Cebuano', 'cs': 'Czech', 'ch_sim': 'Simplified Chinese', 'ch_tra': 'Traditional Chinese',
    'che': 'Chechen', 'cy': 'Welsh', 'da': 'Danish', 'dar': 'Dargwa', 'de': 'German',
    'en': 'English', 'es': 'Spanish', 'et': 'Estonian', 'fa': 'Persian (Farsi)', 'fi': 'Finnish',
    'fr': 'French', 'ga': 'Irish', 'gom': 'Goan Konkani', 'hi': 'Hindi', 'hr': 'Croatian',
    'ht': 'Haitian Creole', 'hu': 'Hungarian', 'id': 'Indonesian', 'inh': 'Ingush',
    'is': 'Icelandic', 'it': 'Italian', 'ja': 'Japanese', 'kbd': 'Kabardian', 'kn': 'Kannada',
    'ko': 'Korean', 'ku': 'Kurdish', 'la': 'Latin', 'lbe': 'Lak', 'lez': 'Lezghian', 'lt': 'Lithuanian',
    'lv': 'Latvian', 'mah': 'Magahi', 'mai': 'Maithili', 'mi': 'Maori', 'mn': 'Mongolian',
    'mr': 'Marathi', 'ms': 'Malay', 'mt': 'Maltese', 'ne': 'Nepali', 'new': 'Newari',
    'nl': 'Dutch', 'no': 'Norwegian', 'oc': 'Occitan', 'pi': 'Pali', 'pl': 'Polish',
    'pt': 'Portuguese', 'ro': 'Romanian', 'ru': 'Russian', 'rs_cyrillic': 'Serbian (Cyrillic)',
    'rs_latin': 'Serbian (Latin)', 'sck': 'Sadri', 'sk': 'Slovak', 'sl': 'Slovenian',
    'sq': 'Albanian', 'sv': 'Swedish', 'sw': 'Swahili', 'ta': 'Tamil', 'tab': 'Tabassaran',
    'te': 'Telugu', 'th': 'Thai', 'tjk': 'Tajik', 'tl': 'Tagalog', 'tr': 'Turkish',
    'ug': 'Uyghur', 'uk': 'Ukrainian', 'ur': 'Urdu', 'uz': 'Uzbek', 'vi': 'Vietnamese'
}


def get_reader(languages):
    """
    Получает или создает экземпляр easyocr.Reader для указанных языков.
    Использует кэширование для предотвращения повторной инициализации.
    :param languages: список или кортеж кодов языков (например, ['ru', 'en', 'de'])
    :return: экземпляр easyocr.Reader или None при ошибке.
    """
    if not languages:  # Если список языков пуст, используем по умолчанию
        languages = ['ru', 'en']

    # Преобразуем список языков в кортеж, чтобы использовать как ключ словаря (неизменяемый тип)
    # Сортируем для консистентности ключа, чтобы ['ru', 'en'] и ['en', 'ru'] давали один результат
    lang_tuple = tuple(sorted(set(languages)))  # set для удаления дубликатов

    if lang_tuple not in reader_cache:
        print(f"Инициализация easyocr.Reader для языков: {list(lang_tuple)}")
        try:
            # gpu=False можно убрать или установить в True, если есть CUDA и PyTorch с поддержкой GPU
            reader_cache[lang_tuple] = easyocr.Reader(list(lang_tuple), gpu=False)
        except Exception as e:
            print(f"Ошибка инициализации easyocr.Reader для {list(lang_tuple)}: {e}")
            # Попытка инициализации с языками по умолчанию в случае ошибки
            try:
                default_langs = ('ru', 'en')
                print(f"Попытка инициализации с языками по умолчанию: {list(default_langs)}")
                reader_cache[default_langs] = easyocr.Reader(list(default_langs), gpu=False)
                return reader_cache[default_langs]
            except Exception as e_default:
                print(f"Ошибка инициализации easyocr.Reader с языками по умолчанию: {e_default}")
                return None  # Возвращаем None, если инициализация не удалась
    else:
        print(f"Использование кэшированного easyocr.Reader для языков: {list(lang_tuple)}")

    return reader_cache[lang_tuple]