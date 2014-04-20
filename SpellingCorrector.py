import re, collections
import sys
import string
import ReadCondProbs

#alphabet = 'abcdefghijklmnopqrstuvwxyz'
symbols = '\'- '
condProbs = ReadCondProbs.getCondProbs('count_1edit.txt', 'count_2l.txt')

def edits1(word):
  splits = []; deletes = []; transposes = [];
  replaces = []; inserts = [];

  for i in range(0, len(word)+1):
    splits.append((word[:i], word[i:]))

  # Deletions
  for a, b in splits:
    if b:
      deletes.append(a + b[1:])

  # Transpositions
  for a, b in splits:
    if (len(b)>1):
      transposes.append(a + b[1] + b[0] + b[2:])

  # Substitutions
  for a, b in splits:
    for c in string.ascii_lowercase:
      if b:
        replaces.append(a + c + b[1:])

  # Insertions
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

#print candidates