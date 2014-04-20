import sys
import os


def getCondProbs(count_1edit, count_2l):
	#count_1edit = str(sys.argv[1])
	#count_2l = str(sys.argv[2])

	fid = open(count_2l, 'r')
	letterCounts = {}
	for line in fid:
		parts = line.split()
		letterCounts[parts[0]] = float(parts[1])
	fid.close()

	tempLC = dict(letterCounts)

	for lc in tempLC:
		if lc[0] in letterCounts:
			letterCounts[lc[0]] += tempLC[lc]
		else:
			letterCounts[lc[0]] = tempLC[lc]


	fid = open(count_1edit, 'r')
	conditionals = {}
	for line in fid:
		parts = line.split()

		count = parts[len(parts) - 1]
		edit = ''
		for p in parts[:len(parts) - 1]:
			edit = edit + p + ' '
		edit = edit[0:len(edit)-1]

		conditionals[edit] = float(count)
	fid.close()

	conditionalProbs={}
	for c in conditionals:
		parts = c.split('|')
		if parts[1] in letterCounts:
			conditionalProbs[c] = conditionals[c]/letterCounts[parts[1]]

	return conditionalProbs