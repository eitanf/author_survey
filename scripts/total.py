#!/usr/bin/env python

import csv
import json
import sys

#turns csv file into list of dictionaries
def todict(file):
	authors = []
	with open(file) as f:
		reader = csv.DictReader(f)
		for row in reader:
			authors.append(row)
		return authors

data = todict(sys.argv[1])
withemail = [item for item in data if item['email'] != '']
print(len(withemail))