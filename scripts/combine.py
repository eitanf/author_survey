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

#writes dict to csv
def dicttocsv(file, dict):
	fields = dict[0].keys()
	print fields
	with open(file, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fields)
		writer.writeheader()
		writer.writerows(dict)

#combine together list of authors and return dict
def combine(a1, a2):
	newdata = []
	for author in a1:
		n = author['name']
		#first we find if there already is an author in the other
		author2 = next((item for item in a2 if item['name'] == n), None)
		if author2 == None: #if not there we just add it
			newdata.append(author)
		else: #in the case they are both there, we combine and add
			author.update(author2)
			newdata.append(author)
	return newdata

if len(sys.argv) < 4:
    print("Required arguments: combine.py file1.csv file2.csv out.csv")
    exit(1)

a1 = todict(sys.argv[1])
a2 = todict(sys.argv[2])
newdata = combine(a2, a1)
dicttocsv(sys.argv[3], newdata)