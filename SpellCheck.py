import tkinter as tk
from tkinter import messagebox
from nltk.corpus import words, brown
from collections import Counter
import nltk
import re

# Download necessary corpora
nltk.download('words')
nltk.download('brown')

# Build the language model
WORDS = Counter(brown.words())

def P(word, N=sum(WORDS.values())):
    """Probability of a word."""
    wp=WORDS[word] / N
    print(wp)
    return wp

def known(words_set):
    """Filter words that are in the corpus."""
    return set(w for w in words_set if w in WORDS)

def edits1(word):
    """Return all strings one edit away from word."""
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def correct(word):
    """Correct the spelling of the word."""
    candidates = known([word]) or known(edits1(word)) or [word]
    return max(candidates, key=P)

def correct_spelling():
    """Button callback to correct spelling from input."""
    input_word = entry.get().lower().strip()
    if not re.match("^[a-z]+$", input_word):
        messagebox.showerror("Input Error", "Please enter a single valid English word.")
        return
    corrected = correct(input_word)
    result_var.set(f"Corrected Word: {corrected}")

# Build GUI
root = tk.Tk()
root.title("Spelling Corrector (Edit Distance + Noisy Channel)")
root.geometry("420x200")

tk.Label(root, text="Enter word to correct:", font=("Helvetica", 12)).pack(pady=10)
entry = tk.Entry(root, width=30, font=("Helvetica", 12))
entry.pack()

tk.Button(root, text="Correct Spelling", command=correct_spelling).pack(pady=10)

result_var = tk.StringVar()
tk.Label(root, textvariable=result_var, font=("Helvetica", 14), fg="green").pack(pady=10)

root.mainloop()
