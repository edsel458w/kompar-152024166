import numpy as np

# NumPy menggunakan SIMD di belakang layar secara otomatis
a = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=np.float32)
b = np.array([10, 20, 30, 40, 50, 60, 70, 80], dtype=np.float32)

# Satu operasi → semua elemen diproses paralel (SIMD internally)
result = a + b

print(result)
# Output: [11. 22. 33. 44. 55. 66. 77. 88.]