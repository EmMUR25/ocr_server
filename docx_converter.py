# docx_converter.py
# Этот модуль требует установки библиотеки: pip install python-docx
from docx import Document
from io import BytesIO

def create_docx_from_text(text_content):
    """
    Создает документ DOCX из предоставленного текста.
    Каждая строка текста (разделенная \n) будет новым абзацем.
    Пустые строки также будут преобразованы в пустые абзацы, сохраняя структуру.

    :param text_content: Строка с текстом для добавления в документ.
    :return: Объект BytesIO, содержащий DOCX файл.
    """
    doc = Document()
    
    # Разделяем текст на строки. Если в тексте есть абзацы, разделенные \n\n,
    # то они превратятся в абзацы с пустыми строками между ними.
    # Если просто строки, то каждая строка станет абзацем.
    lines = text_content.split('\n')
    for line in lines:
        doc.add_paragraph(line)
    
    # Сохраняем документ в поток байтов в памяти
    file_stream = BytesIO()
    doc.save(file_stream)
    file_stream.seek(0) # Перемещаем указатель в начало потока
    return file_stream