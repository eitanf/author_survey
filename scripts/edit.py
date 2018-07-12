##Edit emails so they are only mine!

import sys
import csv

setemail = sys.argv[1]
infile = sys.argv[2]
outfile = sys.argv[3]
fields = ['FirstName', 'LastName', 'PrimaryEmail', 'NumPapers', 'ConferenceName1', 'PaperName1', 'ConferenceName2', 'PaperName2', 'ConferenceName3', 'PaperName3']

authors = []
with open(infile, mode="r", encoding='utf-8') as f:
    reader = csv.DictReader(f)
    authors = list(reader)

for auth in authors:
    auth['PrimaryEmail'] = setemail

with open(outfile, mode="w", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()
    for auth in authors:
        writer.writerow(auth)

