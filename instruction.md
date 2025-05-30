## Инструкция запуска и пример кода
Установка (одна команда):

Для запуска лучше использовать [Анаконду](https://www.anaconda.com/download)

После установки запустите Anaconda.Navigator через пуск

![image](https://github.com/user-attachments/assets/dff0eafa-55e8-4337-8338-422c107537fd)

 перейдите в Anaconda.Navigator -> Environments
 
![image](https://github.com/user-attachments/assets/36361872-bbe6-420b-b815-ff343ff2273e)

Далее кнопка create

![image](https://github.com/user-attachments/assets/83faa5b9-3b3c-439a-8391-c75f9d828c53)

И создаем env:

![image](https://github.com/user-attachments/assets/be706de3-06c4-4ffa-a3c7-a3b0942ca5f2)

Лучше оставить python 3.12.9

Далее в списке всех env выбираем нужное и нажимаем 

![image](https://github.com/user-attachments/assets/8f738cc6-e75e-4d25-9fcd-a9f893f8624e)

И 

![image](https://github.com/user-attachments/assets/1845c8f6-7b5c-461f-ad67-507b8582ebfa)

Открылся терминал выбранного env.

Далее вводим команду установки

```bash
pip install easyocr==1.7.2
```

![image](https://github.com/user-attachments/assets/f5626ffb-4a6a-4fd8-93be-48a783881c4c)

После этого запускаем скрипт

```bash
python ocr_server.py
```

![image](https://github.com/user-attachments/assets/d6f4cc9b-f48e-45af-a311-76e70a00f457)

Далее открываем html файл и закидываем нужный файл

![image](https://github.com/user-attachments/assets/642c301e-c4a5-4bf1-8b55-a398be5cdafd)

Выход

![image](https://github.com/user-attachments/assets/aa128497-d29b-4574-b0a3-f406d36115f4)

