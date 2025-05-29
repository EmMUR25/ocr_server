Динамический выбор языков для OCR
Заголовок: Динамический выбор языков для OCR
Краткое описание: Эта функция позволяет пользователю выбирать языки для распознавания текста непосредственно в веб-интерфейсе. Выбранные языки передаются на сервер, который затем использует easyocr.Reader, инициализированный для этих конкретных языков. Это повышает точность и гибкость OCR. Модуль language_manager.py помогает управлять экземплярами easyocr.Reader для различных наборов языков, используя кэширование для эффективности.
Использование:
Сохраните код выше как language_manager.py в той же директории, что и ocr_server.py.
Модификация index.html:
Добавьте блок для выбора языков перед контейнером загрузки или в другом удобном месте. Можно использовать <select> для множественного выбора или чекбоксы.
<div class="language-selection" style="margin-bottom: 20px; text-align: center;">
    <h3>Выберите языки для распознавания (Ctrl+клик для нескольких):</h3>
    <select id="languageSelector" multiple size="5" style="width: 200px; padding: 5px;">
        </select>
</div>

<div class="divider"></div>
В тег <script> в index.html, добавьте код для заполнения select и сбора выбранных языков:
// В самом начале скрипта, после объявления констант
const languageSelector = document.getElementById('languageSelector');
// Языки из language_manager.py (можно передать их с сервера или захардкодить часть)
const availableLanguages = { /* Скопируйте сюда словарь SUPPORTED_LANGUAGES из language_manager.py */ 
    'en': 'English', 'ru': 'Russian', 'de': 'German', 'fr': 'French', 'es': 'Spanish', 
    'ch_sim': 'Simplified Chinese', 'ja': 'Japanese' // Пример, добавьте больше
}; 

// Заполняем селектор языков
for (const code in availableLanguages) {
    const option = document.createElement('option');
    option.value = code;
    option.textContent = availableLanguages[code];
    if (code === 'ru' || code === 'en') { // Выбираем рус и англ по умолчанию
        option.selected = true;
    }
    languageSelector.appendChild(option);
}

// Внутри функции processImage()
async function processImage() {
    const file = imageInput.files[0];
    if (!file) return;

    resultDiv.textContent = "Идёт распознавание...";
    resultDiv.className = 'loading';

    try {
        const formData = new FormData();
        formData.append('image', file);

        // Собираем выбранные языки
        const selectedLangs = Array.from(languageSelector.selectedOptions).map(opt => opt.value);
        if (selectedLangs.length === 0) { // Если ничего не выбрано, по умолчанию ru, en
            selectedLangs.push('ru', 'en');
        }
        formData.append('languages', JSON.stringify(selectedLangs));

        const response = await fetch('http://localhost:8000/ocr', {
            method: 'POST',
            body: formData
        });
    // ... остальной код processImage
Модификация ocr_server.py:
Удалите глобальную инициализацию: reader = easyocr.Reader(['ru', 'en']).
Импортируйте get_reader из language_manager.py:
from language_manager import get_reader 
# ... другие импорты ...
import json # Убедитесь, что json импортирован
В методе do_POST вашего RequestHandler:
# ...
# form = cgi.FieldStorage(...)

# Получаем языки из формы
selected_languages_json = form.getvalue('languages', '["ru", "en"]') # По умолчанию ru, en
try:
    selected_languages = json.loads(selected_languages_json)
    if not isinstance(selected_languages, list) or not all(isinstance(lang, str) for lang in selected_languages):
        selected_languages = ['ru', 'en'] # Фоллбэк, если данные некорректны
except json.JSONDecodeError:
    selected_languages = ['ru', 'en'] # Фоллбэк при ошибке парсинга

current_reader = get_reader(selected_languages)

if not current_reader:
    self.send_response(500)
    self.send_header('Content-type', 'application/json')
    self.send_header('Access-Control-Allow-Origin', '*')
    self.end_headers()
    self.wfile.write(json.dumps({'error': 'Не удалось инициализировать OCR ридер для выбранных языков.'}).encode())
    return

# Дальше используйте current_reader вместо глобального reader для распознавания
# Пример: results = current_reader.readtext(image, detail=1, paragraph=False)
# ... (логика обработки PDF и изображений с использованием current_reader) ...