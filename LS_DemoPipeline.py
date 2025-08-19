# === Prerequisites ===
# !pip install nltk gensim  # uncomment to install if needed

import nltk
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
from collections import Counter
import numpy as np

# First-time downloads (run once)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)
nltk.download("punkt", quiet=True)

# Optional: load a tiny Word2Vec model for fallback (can be replaced with a larger corpus)
try:
    from gensim.models import Word2Vec
    # toy sentences to get some embeddings
    toy_sentences = [
        ["i", "love", "nlp"],
        ["nlp", "is", "fun"],
        ["i", "love", "ai"],
        ["machine", "learning", "is", "powerful"],
        ["deep", "learning", "makes", "nlp", "better"]
    ]
    w2v_model = Word2Vec(toy_sentences, vector_size=50, window=2, min_count=1, sg=1)
    have_w2v = True
except ImportError:
    print("gensim not installed; embedding similarity will be skipped.")
    have_w2v = False

# --- Utility functions ---

def lesk_disambiguate(sentence, target_word):
    """Return the best synset for target_word in sentence using Lesk."""
    tokens = nltk.word_tokenize(sentence)
    sense = lesk(tokens, target_word)
    return sense

def expand_query(word):
    """Return a set of expansion candidates: synonyms, direct hypernyms, and hyponyms."""
    expansions = set()
    for syn in wn.synsets(word):
        # synonyms (lemmas)
        for lemma in syn.lemmas():
            expansions.add(lemma.name().replace("_", " "))
        # hypernyms
        for h in syn.hypernyms():
            for lemma in h.lemmas():
                expansions.add(lemma.name().replace("_", " "))
        # hyponyms
        for h in syn.hyponyms():
            for lemma in h.lemmas():
                expansions.add(lemma.name().replace("_", " "))
    return expansions

def wn_similarity(w1, w2):
    """Compute highest path similarity over synsets (WordNet)."""
    sims = []
    for s1 in wn.synsets(w1):
        for s2 in wn.synsets(w2):
            sim = s1.path_similarity(s2)
            if sim is not None:
                sims.append(sim)
    return max(sims) if sims else 0.0

def embedding_similarity(w1, w2):
    """Cosine similarity of Word2Vec embeddings if available."""
    if not have_w2v:
        return None
    try:
        v1 = w2v_model.wv[w1]
        v2 = w2v_model.wv[w2]
        cos = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        return float(cos)
    except KeyError:
        return None

# --- Demo pipeline ---

def demo_pipeline(sentence, query_word, candidate_words):
    print(f"> Context sentence: '{sentence}'")
    print(f"> Target word for disambiguation/expansion: '{query_word}'\n")

    # 1. Word Sense Disambiguation with Lesk
    sense = lesk_disambiguate(sentence, query_word)
    if sense:
        print(f"[Lesk] Selected sense: {sense.name()} --> {sense.definition()}")
    else:
        print("[Lesk] No sense found.")

    # 2. Query expansion
    expansions = expand_query(query_word)
    print(f"\n[Expansion] Candidates for '{query_word}':")
    print(", ".join(sorted(list(expansions))[:20]) + ("..." if len(expansions) > 20 else ""))

    # 3. Similarity scoring between query_word and candidate_words
    print("\n[Similarity scores]")
    for cand in candidate_words:
        wn_sim = wn_similarity(query_word, cand)
        emb_sim = embedding_similarity(query_word, cand)
        line = f"  {query_word} ↔ {cand}: WordNet path_sim={wn_sim:.3f}"
        if emb_sim is not None:
            line += f", Embedding cos={emb_sim:.3f}"
        print(line)

# === Example usage ===
sentence1 = "The fisherman sat on the bank of the river."
demo_pipeline(sentence1, "bank", ["financial", "shore", "river", "money"])

sentence2 = "She bought a new car for weekend trips."
demo_pipeline(sentence2, "car", ["vehicle", "bicycle", "automobile", "train"])
