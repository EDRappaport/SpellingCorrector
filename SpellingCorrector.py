import re, collections
import sys
import string

#alphabet = 'abcdefghijklmnopqrstuvwxyz'
symbols = '\'- '

def edits1(word):
  splits = []; deletes = []; transposes = [];
  replaces = []; inserts = [];

   return set(deletes + transposes + replaces + inserts)


#MAIN:
if len(sys.argv) != 2:
  print("Usage: python SpellingCorrector.py <Word>")
  #print("Example: python TC_simpleKNN.py corpus1_train.labels corpus1_test.list")
  sys.exit(-1)

word = str(sys.argv[1])

candidates = edits1(word)

print candidates