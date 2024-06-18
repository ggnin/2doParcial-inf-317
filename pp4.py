import cv2
import numpy as np
from scipy.sparse import csr_matrix


rutaImagenes = 'C:/Users/Mexbol Pcs/Desktop/INF317/parcial 2/'
img1 = cv2.imread(rutaImagenes + 'uno.jpg', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread(rutaImagenes + 'dos.jpg', cv2.IMREAD_GRAYSCALE)


img1 = cv2.resize(img1, (1000, 1000))
img2 = cv2.resize(img2, (1000, 1000))


M = np.float32([[1, 0, 10], [0, 1, 10]])
img2_transformed = cv2.warpAffine(img2, M, (1000, 1000))


m1 = np.array(img1)
m2 = np.array(img2_transformed)


csr1 = csr_matrix(m1)
csr2 = csr_matrix(m2)


mul = csr1.dot(csr2)

print(mul)
print("Numero de elementos no nulos en el resultado:", mul.nnz)

cv2.imshow('Imagen 1', img1)
cv2.imshow('Imagen 2 Transformada', img2_transformed)
cv2.waitKey(0)
cv2.destroyAllWindows()
