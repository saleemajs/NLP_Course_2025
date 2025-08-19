from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

A = np.array([[1,2,3]])
B = np.array([[2,3,4]])
print("Cosine:", cosine_similarity(A, B)[0][0])
