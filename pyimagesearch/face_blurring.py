# Импортируем библиотеки
import numpy as np
import cv2

def anonymize_face_simple(image, factor=3.0):
	# Автоматически определяем размер ядра размытия на
	# основе пространственных размеров входного изображения
	(h, w) = image.shape[:2]
	kW = int(w / factor)
	kH = int(h / factor)

	# Проверяем, что ширина ядра нечётная
	if kW % 2 == 0:
		kW -= 1

	# Проверяем, что высота ядра нечётная
	if kH % 2 == 0:
		kH -= 1

	# Применяем размытие по Гауссу к входному изображению,
	# используя вычисленный размер ядра
	return cv2.GaussianBlur(image, (kW, kH), 0)


def anonymize_face_pixelate(image, blocks=3):
	# Делим входное изображение на блоки NxN
	(h, w) = image.shape[:2]
	xSteps = np.linspace(0, w, blocks + 1, dtype="int")
	ySteps = np.linspace(0, h, blocks + 1, dtype="int")

	# Проходим циклом по блокам в обоих направлениях x и y
	for i in range(1, len(ySteps)):
		for j in range(1, len(xSteps)):
			# Вычисляем начальную и конечную (x, y)-координаты
			# для текущего блока
			startX = xSteps[j - 1]
			startY = ySteps[i - 1]
			endX = xSteps[j]
			endY = ySteps[i]

			# Извлекаем область интереса с помощью среза массива NumPy,
			# вычисляем среднее значение области интереса,
			# рисуем прямоугольник со средним значением RGB
			# в области интереса исходного изображении
			roi = image[startY:endY, startX:endX]
			(B, G, R) = [int(x) for x in cv2.mean(roi)[:3]]
			cv2.rectangle(image, (startX, startY), (endX, endY),
				(B, G, R), -1)

	# Возвращаем запикселеное изображение
	return image