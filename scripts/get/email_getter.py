#!/usr/bin/env python3
#
# Add email addresses to author data.
#
# This script takes a conference short name,and reads in the conf data for it.
# Additionally, it tries to read the XML file and text file that correspond to
# the paper's text, and extract email address from those.
# It also reads in an authors CSV file which may already include emails for the
# authors, and a verified genders file. Finally, it opens up the paper and a
# google query to show the authors data.
#
# It then loops over each paper and each author, and prompts the user to enter
# an email address (or more, comma-separated) for the author, using all the data
# it found in the above files as hints.
# 
# Uses GNU readline to start buffer with existing email, and tab completion cycles xml/gs_email
# (https://pymotw.com/2/readline/)

# Read:
# - previous email and gs_email from survey/authors.csv
# - email from XML data, if found.
# - grep for "@" in txt file.
# - Open paper PDF
# - Fire browser with google

# Prompt for email address, pre-filling the line with previous address.
# - Regular typing: adds addresses, possibly comma-separated
# - Enter: completes editing (if nothing in buffer, then no email; if something, keep)
# - tab: cycle through xml address or gs_email.
# - Then, prompt for gender if not found: M/F/nothing.

# Immediately save email, save gender (if changed).

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

##############################################################################
def display_paper(paper_id):
    fn = paper_path + paper_id + '.pdf'
    if os.path.isfile(fn):
        os.system("/usr/bin/xpdf " + fn + "> /dev/null 2>&1 &" )
    else:
        print("not found! ###################################")


##############################################################################
def complete(text, state):
    global xml_emails
    global txt_emails
    all_emails = list(set(xml_emails + txt_emails ))

    if text == "":
        matches = all_emails
    else:
        matches = [x for x in all_emails if x.startswith(text)]

    # return current completion match
    if state > len(matches):
       return None
    else:
       return matches[state]

def hook():
    global prev_email
    readline.insert_text(prev_email)
    readline.redisplay()

##############################################################################
######### main

class SKIP(Exception):
    pass

if len(sys.argv) < 2:
    print("Required argument: conference name")
    exit(1)

conf = sys.argv[1]
conf_fn = conf_path + conf + ".json"
fieldnames = [ "name", "gs_email", "as_chair", "as_pc", "as_author", "papers", "email" ]

prompt = "ENTER to skip author; (s)kip paper; (q)uit; email (with tab completion)\n >>>"
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

# Read in conference data:
print("Working on conference:", conf_fn)
with open(conf_fn, mode="r", encoding='utf-8') as f:
    confdata = json.load(f)

# Read in pre-existing email data:
with open(author_fn, mode="r", encoding='utf-8') as f:
    reader = csv.DictReader(f)
    authors = list(reader)

# Read in pre-existing gender data:
genders = {}
with open(gender_fn, mode="r", encoding='utf-8') as f:
    genders = json.load(f)

print(confdata)
line = input("Which paper should I skip to? (n/#)")
if line != "n":
	print("Skipping to " + line)
	papers = confdata['papers']
	papers = papers[(int(line)-1):]
	confdata['papers'] = papers
print(confdata)

### Main loop: iterate over all authors, suggest email, and record answer
for paper in confdata['papers']:
    key = paper['key']
    print("\n-----------------------------------------------------------")
    print("Working on paper", key + ":\t" + paper['title'])
    if len(sys.argv) > 2 and key < sys.argv[2]:
        print("skipping...")
        continue

    xml_emails = get_emails_from_xml(key)
    print("Found these emails in the paper's XML data:", xml_emails)

    txt_emails = get_emails_from_text(key)
    print("Found these emails in the paper's text data:", txt_emails)

    display_paper(key)

    try:
        for author in paper['authors']:
            print("\n########################\n### Author:", author)
            name = normalized_author_name(author)

            # Find previous email
            records = [auth for auth in authors if (auth['name'] == name and key in auth['papers'])]
            if len(records) == 0:
                print("Failed to find author record!")
                continue
            rec = records[0]
            prev_email = rec['email']
            gs_email = rec['gs_email']
            print("Previous email:", prev_email, "\tGS email:", gs_email)

            chrome_path = '/usr/bin/chromium %s'

            webbrowser.get(chrome_path).open("http://google.com/search?q=" + author)
            time.sleep(2)
            print()
            line = input(prompt)

            if line == "s" or line == "skip":
                raise SKIP
            elif line == "q" or line == "quit":
                print("Goodbye...")
                os.system("killall xpdf")
                sys.exit(0)

            # Changed email, save file:
            if line != prev_email:
                rec['email'] = line
                with open(author_fn, mode="w", encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                    writer.writeheader()
                    for r in authors:
                        writer.writerow(r)

    except SKIP:
        pass

