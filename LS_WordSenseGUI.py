import tkinter as tk
from tkinter import ttk, scrolledtext
from nltk.corpus import wordnet as wn
from nltk import word_tokenize, pos_tag
from nltk.wsd import lesk
import nltk

# Ensure all NLTK data is downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Sample corpus
corpus = [
    "The bank can guarantee deposits will eventually cover future tuition costs.",
    "After the play, the children ran to the park to enjoy the sunshine.",
    "The rock band played a new song during their concert.",
    "She observed the bat fly across the room in the dim light.",
    "He hit the ball hard and it flew over the fence."
]

# Helpers
def get_open_class_words(sentence):
    tokens = word_tokenize(sentence)
    tagged = pos_tag(tokens)
    return [word for word, tag in tagged if tag.startswith(('NN', 'VB', 'JJ', 'RB'))]

def wordnet_pos(treebank_tag):
    if treebank_tag.startswith('N'):
        return wn.NOUN
    elif treebank_tag.startswith('V'):
        return wn.VERB
    elif treebank_tag.startswith('J'):
        return wn.ADJ
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        return None

def disambiguate_sentence(sentence):
    tokens = word_tokenize(sentence)
    tagged = pos_tag(tokens)
    results = []
    for word, tag in tagged:
        wn_pos = wordnet_pos(tag)
        if wn_pos:
            synset = lesk(tokens, word, pos=wn_pos)
            results.append((word, synset))
    return results

# Tkinter GUI
def run_lesk_gui():
    root = tk.Tk()
    root.title("Word Sense Disambiguation (Lesk Algorithm)")
    root.geometry("900x600")

    tk.Label(root, text="Select a Sentence:", font=('Arial', 12)).pack(pady=5)
    sentence_var = tk.StringVar()
    sentence_dropdown = ttk.Combobox(root, textvariable=sentence_var, width=120, font=('Arial', 10))
    sentence_dropdown['values'] = corpus
    sentence_dropdown.current(0)
    sentence_dropdown.pack(pady=5)

    output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=110, height=30, font=('Courier', 10))
    output.pack(padx=10, pady=10)

    def analyze_sentence():
        output.delete("1.0", tk.END)
        sentence = sentence_var.get()
        output.insert(tk.END, f"Sentence: {sentence}\n\n")
        tagged = pos_tag(word_tokenize(sentence))
        open_words = get_open_class_words(sentence)

        for word, tag in tagged:
            if word not in open_words:
                continue
            wn_pos = wordnet_pos(tag)
            if wn_pos:
                synsets = wn.synsets(word, pos=wn_pos)
                output.insert(tk.END, f"Word: {word} ({tag}) - {len(synsets)} senses\n")
                for i, syn in enumerate(synsets[:5], 1):
                    output.insert(tk.END, f"  {i}. {syn.name()} - {syn.definition()}\n")
            else:
                output.insert(tk.END, f"Word: {word} ({tag}) - No WordNet POS mapping\n")

        output.insert(tk.END, "\nLesk Algorithm Disambiguation:\n")
        lesk_result = disambiguate_sentence(sentence)
        for word, syn in lesk_result:
            if syn:
                output.insert(tk.END, f"  {word} → {syn.name()} - {syn.definition()}\n")
            else:
                output.insert(tk.END, f"  {word} → No sense found\n")

    tk.Button(root, text="Run WSD (Lesk)", command=analyze_sentence, font=('Arial', 12)).pack(pady=5)
    root.mainloop()

# Launch GUI
run_lesk_gui()
