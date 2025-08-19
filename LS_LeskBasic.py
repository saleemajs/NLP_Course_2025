

from nltk.corpus import wordnet as wn
for syn in wn.synsets('bank'):
    print(syn.name(), syn.definition())



from nltk.wsd import lesk

sentence = "The fisherman sat on the bank of the river"
tokens = sentence.split()

sense = lesk(tokens, 'bank')
print(sense)
print("Definition:", sense.definition())
