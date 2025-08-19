from nltk.corpus import wordnet as wn
for syn in wn.synsets('car'):
    print(syn.name(), syn.definition())
