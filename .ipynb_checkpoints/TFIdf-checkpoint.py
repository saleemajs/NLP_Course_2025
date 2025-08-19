from sklearn.feature_extraction.text import TfidfVectorizer
docs = ['NLP is fun','Deep learning is powerful','NLP with deep learning']
X = TfidfVectorizer().fit_transform(docs)
print(X.toarray())
