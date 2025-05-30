import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

from http.server import BaseHTTPRequestHandler, HTTPServer
import easyocr
import cv2
import numpy as np
import json
import cgi

# Инициализация EasyOCR (1 раз при старте)
reader = easyocr.Reader(['ru', 'en'])

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/ocr':
            # Получаем загруженное изображение
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            file_item = form['image']
            image_data = file_item.file.read()
            
            # Конвертируем в OpenCV-формат
            image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
            
            # Распознаём текст с сохранением пробелов
            results = reader.readtext(image, detail=1, paragraph=False)
            output_text = ""
            current_y = 0
            
            for i, (bbox, text, _) in enumerate(results):
                x1, y1 = bbox[0]
                if i > 0 and y1 > current_y + 5:
                    output_text += "\n"
                elif i > 0:
                    output_text += " "
                output_text += text
                current_y = y1
            
            # Отправляем результат
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'text': output_text}).encode())
            
        else:
            self.send_error(404)

    def do_GET(self):
        if self.path == '/':
            # Отдаём HTML-страницу
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)

# Запуск сервера
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Сервер запущен на http://localhost:{port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()