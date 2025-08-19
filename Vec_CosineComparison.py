from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Sample corpus
corpus = [
    "The cat sits on the mat",
    "A cat is on the mat",
    "Dogs are sitting on the rug"
]

# 1. Count-based sparse vectors
count_vec = CountVectorizer()
count_matrix = count_vec.fit_transform(corpus)
count_cosine = cosine_similarity(count_matrix)

# 2. TF-IDF vectors
tfidf_vec = TfidfVectorizer()
tfidf_matrix = tfidf_vec.fit_transform(corpus)
tfidf_cosine = cosine_similarity(tfidf_matrix)

# Print the results
print("Cosine Similarity (Count Vectors):")
print(pd.DataFrame(count_cosine, columns=[f'Doc{i+1}' for i in range(len(corpus))]))

print("\nCosine Similarity (TF-IDF Vectors):")
print(pd.DataFrame(tfidf_cosine, columns=[f'Doc{i+1}' for i in range(len(corpus))]))
