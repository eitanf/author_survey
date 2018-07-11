import csv
import json
import os
import re
import readline
import sys
import time
import webbrowser
import xml.etree.ElementTree as ET

paper_path = "sys-papers/"
conf_path = "conf/"
gender_fn = "verified_gender_mapping.json"
author_fn = "dat.csv"
xml_emails = []
txt_emails = []
fieldnames = [ "name", "gs_email", "as_chair", "as_pc", "as_author", "papers", "email" ]
authors = []

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

# Read in pre-existing email data:
with open(author_fn, mode="r", encoding='utf-8') as f:
    reader = csv.DictReader(f)
    authors = list(reader)
skip = input("Skip to line... ") 
authors2 = authors[int(skip):]
for rec in authors2:
    if len(rec['email']) > 2 or len(rec['gs_email']) < 1:
        continue
    print("\n########################\n### Author:", rec['name'])
    name = normalized_author_name(rec['name'])
    gs_email = rec['gs_email']
    print(gs_email)
    chrome_path = '/usr/bin/chromium %s'
    webbrowser.get(chrome_path).open("http://google.com/search?q=" + name)
    time.sleep(2)
    
    line = input("email: ")
    if line == "s":
        print("Skipping...")
        continue

    #write out
    rec['email'] = line
    with open(author_fn, mode="w", encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames )
        writer.writeheader()
        for r in authors:
            writer.writerow(r) 
