import cv2
import numpy as np

# Subir imágenes
rutaImagenes = 'C:/Users/Mexbol Pcs/Desktop/INF317/parcial 2/'
img1 = cv2.imread(rutaImagenes + 'uno.jpg')
img2 = cv2.imread(rutaImagenes + 'dos.jpg')

# Redimensionar las imágenes al mismo tamaño
img1 = cv2.resize(img1, (200, 200))
img2 = cv2.resize(img2, (200, 200))

# Sumar
alpha = 0.5  
beta = 1 - alpha  
suma = cv2.addWeighted(img1, alpha, img2, beta, 0)

# Restar
resta = cv2.absdiff(img1, img2)

# Mostrar
cv2.imshow('imagen1', img1)
cv2.imshow('imagen2', img2)
cv2.imshow('Suma', suma)
cv2.imshow('Resta', resta)
cv2.waitKey(0)
cv2.destroyAllWindows()

