# FirstName,LastName,PrimaryEmail,ExternalDataReference,EmbeddedDataA,EmbeddedDataB

import csv
import string
from pdfrw import PdfReader
import json

paperpath = '../sys-papers/'
datapath = '../dat.csv'
confpath = '../conf/'
fields = ['FirstName', 'LastName', 'PrimaryEmail', 'NumPapers', 'ConferenceName1', 'PaperName1', 'ConferenceName2', 'PaperName2', 'ConferenceName3', 'PaperName3']
##Takes a dictionary that contains the correct fields and writes to the output file
def write(author_dict, out):
    with open(out, mode="w", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        for auth in author_dict:
            writer.writerow(auth)

#Read in pre-existing data from csv
def read_csv(in_file):
    with open(in_file, mode="r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        authors = list(reader)
    return authors

def grab_paper_name(key):
    conf = key.split('_')[0]
    with open(confpath + conf + ".json", mode = "r", encoding = "utf-8") as f:
        dat = json.load(f)
        papers = dat['papers']
        p = next(pap for pap in papers if pap['key'] == key)
        title = p['title']
        return title

##Creates correct dict from a raw data dictionary 
def create(in_dict):
    out = {}
    
    ##Collect and process input data
    name = in_dict['name']
    first_name = name.split(",")[0]
    last_name = name.split(",")[1]
    
    emails_raw = in_dict['email']
    if emails_raw == '':
        return 0
    emails = []
    if "," in emails_raw:
        emails = emails_raw.split(",")
    else:
        emails.append(emails_raw) 
    papers_raw = in_dict['papers']
    papers = []
    if "," in papers_raw:
        papers = papers_raw.split(",")
    else:
        papers.append(papers_raw)

    out['FirstName'] = first_name
    out['LastName'] = last_name
    out['PrimaryEmail'] = emails[0]
    out['NumPapers'] = len(papers)
    on = 1
    for p in papers: #External data comes in pairs of two, eg: B, C then D, E.... first is always paper, second is name
        out['ConferenceName' + str(on)] = p.split("_")[0]
        out['PaperName' + str(on)] = grab_paper_name(p)
        on = on + 1

    return out
authors = read_csv(datapath)
#print(create(authors[10]))

#test get 100 into csv file
out_dicts = []
for auth in authors[10:110]:
    out_dict = create(auth)
    if out_dict != 0:
        out_dicts.append(out_dict)

write(out_dicts, "out.csv")
