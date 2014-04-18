import re, collections
import sys
import string

#alphabet = 'abcdefghijklmnopqrstuvwxyz'
symbols = '\'- '

def edits1(word):
  splits = []; deletes = []; transposes = [];
  replaces = []; inserts = [];

  for i in range(0, len(word)+1):
    splits.append([(word[:i], word[i:])])

  for a, b in splits:
    if b:
      deletes.append(a + b[1:])

  for a, b in splits:
    if (len(b)>1):
      transposes.append(a + b[1] + b[0] + b[2:])

  for a, b in splits:
    for c in string.ascii_lowercase:
      if b:
        replaces.append(a + c + b[1:])

  for a, b in splits:
      for c in string.ascii_lowercase:
        inserts.append(a + c + b)

   return set(deletes + transposes + replaces + inserts)


#MAIN:
if len(sys.argv) != 2:
  print("Usage: python SpellingCorrector.py <Word>")
  #print("Example: python TC_simpleKNN.py corpus1_train.labels corpus1_test.list")
  sys.exit(-1)

word = str(sys.argv[1])

candidates = edits1(word)

print candidates