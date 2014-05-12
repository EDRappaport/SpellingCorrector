import re, collections
import sys
import string
import math
import ReadCondProbs
import NGramProbs

#alphabet = 'abcdefghijklmnopqrstuvwxyz'
symbols = '\'- '
condProbs = ReadCondProbs.getCondProbs('count_1edit.txt', 'count_2l.txt')

def edits1(word):
  splits = []; deletes = []; transposes = [];
  replaces = []; inserts = [];
  probs = {};

  for i in range(0, len(word)+1):
    splits.append((word[:i], word[i:]))


  # Insertions
  for a, b in splits:
    if b:
      inserts.append(a + b[1:])
      insertedLetter = b[0]
      if a:
        biLGram = a[len(a)-1] + b[0]
        if biLGram+'|'+a[len(a)-1] in condProbs:
          probs[a + b[1:]] = condProbs[biLGram+'|'+a[len(a)-1]]
        #else:
          #print "Ain't Here"



  # Transpositions
  for a, b in splits:
    if (len(b)>1):
      transposes.append(a + b[1] + b[0] + b[2:])
      if b[0] + b[1] + '|' + b[1] + b[0] in condProbs:
        probs[a + b[1] + b[0] + b[2:]] = condProbs[b[0] + b[1] + '|' + b[1] + b[0]]
      


  # Substitutions
  for a, b in splits:
    for c in string.ascii_lowercase:
      if b:
        replaces.append(a + c + b[1:])
        if b[0] + '|' + c in condProbs:
          probs[a + c + b[1:]] = condProbs[b[0] + '|' + c]


  # Deletions
  for a, b in splits:
      for c in string.ascii_lowercase:
        deletes.append(a + c + b)
        if a:
          if a[len(a)-1] + '|' + a[len(a)-1] + c in condProbs:
            probs[a + c + b] = condProbs[a[len(a)-1] + '|' + a[len(a)-1] + c]


  #return set(inserts + transposes + replaces + deletes)
  return probs


#MAIN:
if len(sys.argv) != 3:
  print("Usage: python SpellingCorrector.py <Word>")
  #print("Example: python TC_simpleKNN.py corpus1_train.labels corpus1_test.list")
  sys.exit(-1)

word1 = str(sys.argv[1])
word2 = str(sys.argv[2])

probs = edits1(word1)

maxProb = -10000000000
bestWord = word1
for p in probs:
  p1 = float(NGramProbs.getBiGramProb("_START_ " + p))
  p2 = float(NGramProbs.getBiGramProb(p + " " + word2))

  print p
  print p1
  print p2

  if (p1 != 0) & (p2 != 0):
    curP = math.log10(p1) + math.log10(p2) + math.log10(float(probs[p]))
    if curP > maxProb:
      maxProb = curP
      bestWord = p

print maxProb
print bestWord
