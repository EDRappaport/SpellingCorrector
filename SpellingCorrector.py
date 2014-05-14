import re, collections
import sys
import os
import string
import math
import nltk
import Queue
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

words=[]

if len(sys.argv) > 3:
  fileList = os.listdir(sys.argv[3])
  for f in fileList:
    fid = open(sys.argv[3]+f)
    text = fid.read()
    for w in text.split():
      words.append(w.lower())

text = nltk.corpus.brown.words()
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
  sentProbs = []
  for i in range(len(sentence)):
    sentence[i] = sentence[i].lower()
    editProbs.append(.0000001)
    probs = edits1(sentence[i])
    probs[sentence[i]] = .0000001
    sentProbs.append(probs)

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

      #probs = edits1(curWord)
      probs = sentProbs[i]

      maxProb = 0
      bestProbs = Queue.PriorityQueue(3)
      bestProbs.put_nowait([0, ""])
      bestProbs.put_nowait([0, ""])
      bestProbs.put_nowait([0, ""])

      bestWord = curWord
      ep = editProbs[i]

      probs[curWord] = editProbs[i]

      for p in probs:

        #Smoothing:
        f1 = cfd[prevWord][p]
        t1 = cfd[prevWord].N()
        #if t1 == 0:
        if t1 < 5:
          t1 = 1000
        if f1 == 0:
          f1 = .0001
          t1=t1+1

        f2 = cfd[p][nextWord]
        t2 = cfd[p].N()
        #if t2 == 0:
        if t2 < 5:
          t2 = 1000
        if f2 == 0:
          f2 = .0001
          t2=t2+1
        #

        p1 = float(f1)/float(t1)
        p2 = float(f2)/float(t2)
        #curP = math.pow(p1, 2) * probs[p] * math.pow(p2, 2)
        curP = p1 * probs[p] * p2
        currentMin = bestProbs.get(False)
        if curP > currentMin[0]:
          bestProbs.put_nowait([curP, p])
          ep = probs[p]

        else:
          bestProbs.put_nowait(currentMin)


      w1 = bestProbs.get(False);
      w2 = bestProbs.get(False);
      w3 = bestProbs.get(False);

      bestWord = w3[1]

      bestProbs.put_nowait(w1)
      bestProbs.put_nowait(w2)
      bestProbs.put_nowait(w3)

      
      if bestWord != sentence[i]:
        changed =True
        sentence[i] = bestWord
        editProbs[i] = ep

      if i == len(sentence) - 1:
        #fidOut.write(bestWord+"\n")
        fidOut.write("{" + bestProbs.get(False)[1] + ", " + bestProbs.get(False)[1] + ", " + bestProbs.get(False)[1] + "}\n")
      else:
        fidOut.write("{" + bestProbs.get(False)[1] + ", " + bestProbs.get(False)[1] + ", " + bestProbs.get(False)[1] +"} ")
        #fidOut.write(bestWord+" ")
