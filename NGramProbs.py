from ast import literal_eval
import re
import requests
import subprocess
import sys

def getBiGramProb(words):
	params = dict(content=words,year_start=2007,year_end=2008, corpus=17, smoothing=3, case_insensitive=True)
	req = requests.get('http://books.google.com/ngrams/graph', params=params)
	res = re.findall('var data = (.*?);\\n', req.text)

	if len(res) > 0:
		if len(literal_eval(res[0])) > 0:
			if len(literal_eval(res[0])[0]['timeseries']) > 0:
				return literal_eval(res[0])[0]['timeseries'][0]

	return 0
