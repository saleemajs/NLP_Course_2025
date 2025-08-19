import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output

def update_heatmap(corpus_text):
    docs = [line.strip() for line in corpus_text.split('\n') if line.strip()]
    if len(docs) < 2:
        print("Please provide at least 2 non-empty documents (one per line).")
        return
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(docs)
    sim_matrix = cosine_similarity(X)
    labels = [f"Doc{i+1}" for i in range(len(docs))]
    sim_df = pd.DataFrame(sim_matrix, index=labels, columns=labels)
    display(sim_df)  # show similarity matrix
    plt.figure(figsize=(6, 5))
    plt.imshow(sim_matrix, aspect='equal', interpolation='nearest')
    plt.title("Cosine Similarity Heatmap (Count-Based Vectors)")
    plt.xlabel("Documents")
    plt.ylabel("Documents")
    plt.xticks(ticks=np.arange(len(docs)), labels=labels, rotation=45)
    plt.yticks(ticks=np.arange(len(docs)), labels=labels)
    plt.colorbar(label="Cosine similarity")
    plt.tight_layout()
    plt.show()

default_docs = [
    "the cat sat on the mat",
    "the dog sat on the log",
    "cats and dogs are pets",
    "the bird sang a song",
    "pets like cats and dogs"
]
default_text = "\n".join(default_docs)

textarea = widgets.Textarea(
    value=default_text,
    description="Corpus (one per line):",
    layout=widgets.Layout(width='100%', height='200px'),
    style={'description_width': 'initial'}
)
button = widgets.Button(description="Update Heatmap", button_style='primary')
output = widgets.Output()

def on_button_clicked(b):
    with output:
        clear_output(wait=True)
        update_heatmap(textarea.value)

button.on_click(on_button_clicked)
display(widgets.VBox([textarea, button, output]))
