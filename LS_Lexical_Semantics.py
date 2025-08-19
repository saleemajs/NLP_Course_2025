from nltk.corpus import wordnet as wn

def explore_word(word):
    print(f"Word: {word}")
    for syn in wn.synsets(word):
        print(f"  Synset: {syn.name()} - {syn.definition()}")
        print(f"    Lemmas: {[l.name() for l in syn.lemmas()]}")
        print(f"    Hypernyms: {[h.name().split('.')[0] for h in syn.hypernyms()]}")
        print(f"    Hyponyms: {[h.name().split('.')[0] for h in syn.hyponyms()[:3]]} ...")
        print(f"    Antonyms: {[a.name() for l in syn.lemmas() for a in l.antonyms()]}")
        print(f"    Meronyms: {[m.name().split('.')[0] for m in syn.part_meronyms()]}")
        print(f"    Holonyms: {[h.name().split('.')[0] for h in syn.part_holonyms()]}")
        print("---")

# Example: explore semantic relations of 'dog' and 'big'
explore_word("dog")
explore_word("big")
