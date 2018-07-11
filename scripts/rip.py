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
author_fn = "authors-with-email.csv"
xml_emails = []
txt_emails = []

##############################################################################
# parse_author_name(): break an author string to a name, and potentially also
# an affiliation string (in parenthesis).
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

##############################################################################
# normalize_author_name(): break an author string to a name and (optional)
# affiliation, and return the name only, last first, title case, no honorifics
def normalized_author_name(name):
    recased = name.title().replace('Jr.', '').replace('Sr.', '').replace('Dr.', '').replace('Prof.', '')
    names = parse_author_name(recased)[0].split()
    return names[-1] + ", " + " ".join(names[:-1])


##############################################################################
# Read in emails from paper XML data:
def get_emails_from_xml(paper_id):
    xml_emails = []
    fn = paper_path + paper_id + ".cermxml"
    tree = ET.parse(fn)
    root = tree.getroot()

    for i in root.findall('./front/article-meta/contrib-group/contrib/'):
        if i.tag == 'email':
            xml_emails.append(i.text)

    return xml_emails

##############################################################################
# Read in emails from paper XML data:
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

if len(sys.argv) < 2:
    print("Required argument: conference name")
    exit(1)

conf = sys.argv[1]
conf_fn = conf_path + conf + ".json"
fieldnames = [ "name", "gs_email", "as_chair", "as_pc", "as_author", "papers", "email" ]

prompt = "ENTER to skip author; (s)kip paper; (q)uit; email (with tab completion)\n >>>"

# Read in conference data:
print("Working on conference:", conf_fn)
with open(conf_fn, mode="r", encoding='utf-8') as f:
    confdata = json.load(f)

# Read in pre-existing email data:
with open(author_fn, mode="r", encoding='utf-8') as f:
    reader = csv.DictReader(f)
    authors = list(reader)

for paper in confdata['papers']:
    key = paper['key']
    print("\n-----------------------------------------------------------")
    print("Working on paper", key + ":\t" + paper['title'])

    xml_emails = get_emails_from_xml(key)
    print("Found these emails in the paper's XML data:", xml_emails)

    txt_emails = get_emails_from_text(key)
    print("Found these emails in the paper's text data:", txt_emails)

    if(len(paper['authors']) <= len(txt_emails)):
        #prompt emails
        i = 0
        print("hit")
        for auth in paper['authors']:
            name = normalized_author_name(auth)
            #find author record
            records = [auth for auth in authors if (auth['name'] == name and key in auth['papers'])]
            if len(records) != 0:
                record = records[0]
                line = input(name + " " + txt_emails[i]+ "? ")
                if line == 'y':
                   record['email'] = txt_emails[i]
            i = i + 1

    	#write out to papers
        with open(author_fn, mode="w", encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in authors:
                writer.writerow(r)