import re, collections
import sys
import os
import string
import math
import nltk
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
  #sys.exit(-1)

text = nltk.corpus.brown.words()
words = []
for w in text:
  words.append(w.lower())
text = nltk.corpus.reuters.words()
for w in text:
  words.append(w.lower())
text = nltk.corpus.gutenberg.words()
for w in text:
  words.append(w.lower())
bigrams = nltk.bigrams(words)
cfd = nltk.ConditionalFreqDist(bigrams)


sentenceFile = str(sys.argv[1])
fidIn = open(sentenceFile, 'r')

outputFile = str(sys.argv[2])
fidOut = open(outputFile, 'w')

#sentence = sys.argv[1:]
for line in fidIn:
  sentence = string.split(line)
  editProbs = []
  for i in range(len(sentence)):
    editProbs.append(.0000001)

  changed = True
  while changed == True:
    changed = False
    for i in range(len(sentence)):
      curWord = sentence[i].lower()
      if i == 0:
        prevWord = '.'
      else:
        prevWord = sentence[i-1].lower()

      if i == len(sentence) - 1:
        nextWord = '.'
      else:
        nextWord = sentence[i+1].lower()

      probs = edits1(curWord)

      maxProb = 0
      bestWord = curWord
      ep = editProbs[i]
      #probs[curWord] = .0000001
      probs[curWord] = editProbs[i]
      for p in probs:

        #Smoothing:
        f1 = cfd[prevWord][p]
        t1 = cfd[prevWord].N()
        if t1 == 0:
          t1 = 1000
        if f1 == 0:
          f1 = .001
          t1=t1+1

        f2 = cfd[p][nextWord]
        t2 = cfd[p].N()
        if t2 == 0:
          t2 = 1000
        if f2 == 0:
          f2 = .001
          t2=t2+1
        #

        p1 = float(f1)/float(t1)
        p2 = float(f2)/float(t2)
        #curP = math.pow(p1, 2) * probs[p] * math.pow(p2, 2)
        curP = p1 * probs[p] *p2
        #print curWord + "- " + p +"; p1 = " + str(p1) + "; p2 = " + str(p2) +";  " + str(probs[p])
        if curP > maxProb:
          maxProb = curP
          bestWord = p
          ep = probs[p]


      print maxProb
      print bestWord
      editProbs[i] = ep
      if bestWord != sentence[i]:
        changed =True
        sentence[i] = bestWord

      if i == len(sentence) - 1:
        fidOut.write(bestWord+"\n")
      else:
        fidOut.write(bestWord+" ")
