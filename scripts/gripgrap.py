import csv
import json
import os
import re
import readline
import sys
import time
import webbrowser
import xml.etree.ElementTree as ET
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

paper_path = "sys-papers/" 
conf_path = "conf/" 
gender_fn = "verified_gender_mapping.json"
author_fn = "dat.csv"
xml_emails = []
txt_emails = []

def parse_author_name(person):
    if re.match("[a-z]*\(", person) is not None or \
            re.match(".*\(.*[a-zA-Z ]$", person) is not None or \
            re.match(" and ", person):
                print("\t\t!!!!!!!!!! Possibly malformed name:", person)

    m = re.match("([^\(]*) \((.*)\)$", person)
    if m is None:
        return person, None
    else:
        return m.group(1), m.group(2)
def normalized_author_name(name):
    recased = name.title().replace('Jr.', '').replace('Sr.', '').replace('Dr.', '').replace('Prof.', '')
    names = parse_author_name(recased)[0].split()
    return names[-1] + ", " + " ".join(names[:-1])
def display_paper(paper_id):
    fn = paper_path + paper_id + '.pdf'
    if os.path.isfile(fn):
        os.system("/usr/bin/xpdf " + fn + "> /dev/null 2>&1 &" )
    else:
        print("not found! ###################################")
def get_emails_from_text(paper_id):
    txt_emails = []
    fn = paper_path + paper_id + ".txt"

    with open(fn, "r") as f:
        for line in f:
            for e in re.findall(r"[^@]+@[^@\s,]+\.[^@\s,]+", line):
                m = re.search(r"[\{\(]([^{^}]+)[\}\)]([@]\S*)", e)
                if m:
                    for name in m.group(1).split(','):
                        txt_emails.append(name.strip(' ,') + m.group(2))
                else:
                    txt_emails.append(e.strip(',').split()[-1])

    return txt_emails
def get_emails_from_xml(paper_id):
    xml_emails = []
    fn = paper_path + paper_id + ".cermxml"
    tree = ET.parse(fn)
    root = tree.getroot()

    for i in root.findall('./front/article-meta/contrib-group/contrib/'):
        if i.tag == 'email':
            xml_emails.append(i.text)

    return xml_emails

if len(sys.argv) < 2:
    print("Required argument: conference name")
    exit(1)

conf = sys.argv[1]
conf_fn = conf_path + conf + ".json"
fieldnames = [ "name", "gs_email", "as_chair", "as_pc", "as_author", "papers", "email" ]

# Read in conference data:
print("Working on conference:", conf_fn)
with open(conf_fn, mode="r", encoding='utf-8') as f:
    confdata = json.load(f)

# Read in pre-existing email data:
with open(author_fn, mode="r", encoding='utf-8') as f:
    reader = csv.DictReader(f)
    authors = list(reader)

line = input("Which paper should I skip to? (n/#)")
if line != "n":
        print("Skipping to " + line)
        papers = confdata['papers']
        papers = papers[(int(line)-1):]
        confdata['papers'] = papers

for paper in confdata['papers']:
    key = paper['key']
   ## display_paper(key)
    print("working on paper: " + key)
    xml_emails = get_emails_from_xml(key)
    txt_emails = get_emails_from_text(key)
    setbreak = False

    for author in paper['authors']:
        if setbreak == True:
            break
        name = normalized_author_name(author)
        records = [auth for auth in authors if (auth['name'] == name and key in auth['papers'])]
        if len(records) == 0:
            print("Failed to find author record!")
            continue
        rec = records[0]
        
        if len(rec['email']) > 0:
            continue
        notgood = True
        tests = process.extract(name, xml_emails) + process.extract(name, txt_emails)
        tests_sorted = sorted(tests, key=lambda trys: trys[1], reverse=True)
            
        while notgood == True:
            if len(tests_sorted) < (len(paper['authors'] ) - 1):
                print("Paper has empty email data!")
                setbreak = True
                break
            
            print(name + " " + tests_sorted[0][0] + " " + rec['email'])
            line = input("all good? ")
            if line != "e" != "n":
                if line == "y":
                    rec['email'] = tests_sorted[0][0]
                if line == "w": 
                    ins = input("Enter email ") 
                    rec['email'] = ins
                if line == "a":
                    rec['email'] = rec['email'] + "," +tests_sorted[0][0]
                with open(author_fn, mode="w", encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                    writer.writeheader()
                    for a in authors:
                        writer.writerow(a)
                notgood = False
            if line == "e": 
                notgood = False
