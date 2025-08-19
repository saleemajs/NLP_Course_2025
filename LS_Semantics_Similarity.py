from nltk.corpus import wordnet as wn
for syn in wn.synsets('car'):
    print(syn.name(), syn.definition())

from nltk.wsd import lesk
sentence = "I need to buy a new car"
sense = lesk(sentence.split(), 'car')
print(sense, sense.definition())

#WSD
#Query Expansion in IR
synsets = wn.synsets('car')
synonyms = set()
for syn in synsets:
    for lemma in syn.lemmas():
        synonyms.add(lemma.name())
print("Query expansion candidates:", synonyms)
#semantic similarity
car = wn.synset('car.n.01')
automobile = wn.synset('automobile.n.01')
print("Path similarity:", car.path_similarity(automobile))

#Ontology
for path in car.hypernym_paths():
    print(" > ".join([p.name().split('.')[0] for p in path]))



