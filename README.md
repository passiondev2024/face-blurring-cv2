![прямоугольник](https://github.com/SINikiforov/face-blurring-opencv/assets/117852442/6bafa580-d304-469d-a720-d43e1808c012)# Face Blurring

Face Blurring - это простое приложение для размытия лиц на видеозаписи с использованием OpenCV и библиотеки Tkinter для графического интерфейса.

## Описание

Это приложение предоставляет пользователю возможность запускать видеозапись с веб-камеры и обрабатывать ее, размывая обнаруженные лица. Пользователь может выбрать метод обработки (Simple или Pixelated), задать количество блоков (для метода Pixelated) и порог точности для определения лиц.

## Требования

Для запуска приложения вам понадобятся следующие библиотеки:

- OpenCV
- Tkinter
- imutils
- numpy

Вы можете установить их с помощью pip:

```bash
pip install opencv-python
pip install numpy
pip install imutils
```

Склонируйте репозиторий с приложением на свой компьютер:
```bash
git clone https://github.com/SINikiforov/face-blurring-opencv.git
cd face-blurring-opencv
```

## Запуск

Для запуска приложения выполните следующую команду:

```bash
python3 main.py
```

## Использование

1. Запустите приложение с помощью указанных выше инструкций.
2. Выберите метод обработки (Simple или Pixelated).
3. Установите количество блоков (для метода Pixelated) и порог уверенности.
4. Нажмите кнопку "Start" для начала обработки видеозаписи.
5. Нажмите кнопку "Stop" для завершения обработки.

## Пример работы приложения

![Пример_размытия](https://github.com/SINikiforov/face-blurring-opencv/assets/117852442/b4f3eb4c-cba2-443c-8c95-83f3544354da)
![Пример_размытия_pixel](https://github.com/SINikiforov/face-blurring-opencv/assets/117852442/45d2d75e-bbf8-41ff-afc3-5b0be64bdd29)

## Автор

Автор проекта: [Sergey Nikiforov]

