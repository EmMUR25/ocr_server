from http.server import HTTPServer, BaseHTTPRequestHandler
import easyocr
import cv2
import numpy as np
import cgi
import json

reader = easyocr.Reader(['ru', 'en'])

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/ocr':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            file_item = form['image']
            image_data = file_item.file.read()
            
            image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
            
            results = reader.readtext(image, detail=1, paragraph=False)
            output_text = " ".join([text for (_, text, _) in results])
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'text': output_text}).encode())
            
        else:
            self.send_error(404)

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Сервер запущен на http://localhost:{port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()