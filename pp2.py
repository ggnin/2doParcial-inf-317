import cv2
import numpy as np
from scipy.sparse import csr_matrix

rutaImagenes = 'C:/Users/Mexbol Pcs/Desktop/INF317/parcial 2/'
imagen1 = cv2.imread(rutaImagenes + 'uno.jpg', cv2.IMREAD_GRAYSCALE)
imagen2 = cv2.imread(rutaImagenes + 'dos.jpg', cv2.IMREAD_GRAYSCALE)


imagen1=cv2.resize(imagen1, (500, 500))
imagen2=cv2.resize(imagen2, (500, 500))

matriz = np.array(imagen1) + np.array(imagen2)

csr = csr_matrix(matriz)
print(csr)