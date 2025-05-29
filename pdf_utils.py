# pdf_utils.py
# Этот модуль требует установки библиотек: pip install pdf2image Pillow
# Также может потребоваться установка Poppler: https://pdf2image.readthedocs.io/en/latest/installation.html

from pdf2image import convert_from_bytes
import numpy as np
import cv2


def convert_pdf_to_images_for_ocr(pdf_bytes):
    """
    Конвертирует PDF-документ (в виде байтов) в список изображений,
    готовых для OCR с использованием OpenCV/EasyOCR.

    :param pdf_bytes: Байты PDF файла.
    :return: Список изображений в формате NumPy array (BGR) или пустой список при ошибке.
    """
    images_for_ocr = []
    try:
        # Конвертируем PDF из байтов в список объектов PIL Image
        pil_images = convert_from_bytes(pdf_bytes)

        for pil_image in pil_images:
            # Конвертируем PIL Image в NumPy array (OpenCV формат - BGR)
            open_cv_image = np.array(pil_image)
            # Конвертируем RGB (из PIL) в BGR (для OpenCV)
            if open_cv_image.shape[2] == 3:  # Проверяем, что это цветное изображение
                open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
            elif open_cv_image.shape[2] == 4:  # Если есть альфа-канал (RGBA)
                open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGBA2BGR)
            images_for_ocr.append(open_cv_image)

    except Exception as e:
        print(f"Ошибка при конвертации PDF в изображения: {e}")
        return []

    return images_for_ocr