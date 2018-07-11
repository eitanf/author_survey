# FirstName,LastName,PrimaryEmail,ExternalDataReference,EmbeddedDataA,EmbeddedDataB

import csv
import string
from pdfrw import PdfReader

fields = ['FirstName', 'LastName', 'PrimaryEmail', 'ExternalDataReference', 'EmbeddedDataA', 'EmbeddedDataB']
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

def grab_paper_name_text(key):
    with open("sys-papers/" + key + ".txt", mode = "r", encoding = "utf-8") as f:
        content = f.readlines()
        title = content[2] + content[3]
    print(title)
    return title

def grab_paper_name_pdf(key):
    reader = PdfReader("sys-papers/" + key + ".pdf")
    
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
    out['ExternalDataReference'] = '' #Add exn here at some point...
    out['EmbeddedDataA'] = len(papers)
    on = 1
    alph_upper =  list(string.ascii_uppercase)
    for p in papers: #External data comes in pairs of two, eg: B, C then D, E.... first is always paper, second is name
        out['EmbeddedData' + alph_upper[on]] = p
        on = on + 1
       ## out['EmbeddedData' + alph_upper[on]] = grab_paper_name(p)
        on = on + 1

    return out
authors = read_csv("dat.csv")
create(authors[10])

#test get 100 into csv file
out_dicts = []
for auth in authors[10:110]:
    out_dict = create(auth)
    if out_dict != 0:
        out_dicts.append(out_dict)

write(out_dicts, "out.csv")
