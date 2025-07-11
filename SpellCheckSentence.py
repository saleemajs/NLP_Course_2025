import tkinter as tk
from tkinter import messagebox, scrolledtext
from nltk.corpus import brown
from collections import Counter
import nltk
import re

# Download required data
nltk.download('brown')

# Build language model from Brown corpus
WORDS = Counter(w.lower() for w in brown.words())

def P(word, N=sum(WORDS.values())):
    """Probability of `word`."""
    return WORDS[word] / N

def known(words_set):
    """Return the subset of words that appear in the dictionary."""
    return set(w for w in words_set if w in WORDS)

def edits1(word):
    """All edits that are one edit away from `word`."""
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:]           for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:]  for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:]      for L, R in splits if R for c in letters]
    inserts = [L + c + R           for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    """All edits that are two edits away from `word`."""
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def candidates(word):
    """Generate possible spelling corrections for word."""
    return (known([word]) or
            known(edits1(word)) or
            known(edits2(word)) or
            [word])

def correct(word):
    """Most probable spelling correction for word."""
    return max(candidates(word), key=P)

def is_valid_word(word):
    return bool(re.match("^[a-zA-Z]+$", word))

def correct_sentence():
    input_text = entry.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showerror("Input Error", "Please enter some text.")
        return

    words_in_input = re.findall(r'\b\w+\b', input_text.lower())
    corrected_words = []
    highlighted_output = ""

    for word in words_in_input:
        if not is_valid_word(word):
            corrected_words.append(word)
            highlighted_output += word + " "
            continue
        corrected = correct(word)
        if corrected != word:
            corrected_words.append(corrected)
            highlighted_output += f"[{corrected}]"  # highlight corrected word
        else:
            corrected_words.append(word)
            highlighted_output += word
        highlighted_output += " "

    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, highlighted_output.strip())
    messagebox.showinfo("Spell Check Complete", "Highlighted words were corrected!")

# GUI setup
root = tk.Tk()
root.title("Enhanced Spelling Corrector")
root.geometry("700x400")

tk.Label(root, text="Enter your sentence:", font=("Helvetica", 12)).pack(pady=10)
entry = scrolledtext.ScrolledText(root, width=80, height=6, font=("Helvetica", 12))
entry.pack()

tk.Button(root, text="Correct Spelling", command=correct_sentence, font=("Helvetica", 11), bg="#4CAF50", fg="white").pack(pady=10)

tk.Label(root, text="Corrected Output (Corrected words shown in [brackets]):", font=("Helvetica", 12)).pack(pady=5)
result_box = scrolledtext.ScrolledText(root, width=80, height=6, font=("Helvetica", 12), fg="darkgreen")
result_box.pack()

root.mainloop()
