#basic python script for interfacing with qualtrics using the API

import os
import requests

#global variables - the API token we need and the data center variable
apiToken = os.environ["Q_API_TOKEN"] # 1
dataCenter = os.environ["Q_DATA_CENTER"]  # 2

#the url of the API f
baseUrl = "https://{0}.qualtrics.com/API/v3/surveys".format(dataCenter)

#open pre-existing author data
authors = []
with open(author_fn, mode="r", encoding='utf-8') as f:
    	reader = csv.DictReader(f)
    	authors = list(reader)

#take a generate files and import them into qualtrics using a POST request
#default type - 'application/vnd.qualtrics.survey.qsf'
def import_survey(files, type):
	headers = {
    	"x-api-token": apiToken,
    }
    responses = []
    for f in files:
		f_dict = {
    		'file': (f, open(f, 'rb'), type)
  		}

		data = { "name": "Test" }
		response = requests.post(baseUrl, files=files, data=data, headers=headers)
		responses.append(response)

	return response

#take a survey and update its data
def update(surveyID, data):
	headers = {
    "content-type": "application/json",
    "x-api-token": apiToken,
    }
    url = baseUrl.format(surveyID)
	response = requests.put(url, json=data, headers=headers)
	return response

#delete by survey ID
def delete(surveyID):
	headers = {
	    "content-type": "application/json",
    	"x-api-token": apiToken,
    }

    url = baseUrl.format(surveyID)
	response = requests.delete(url, headers=headers)
	return response


#take an author email and form a survey, outputting to an advanced txt file for importing into qualtrics
def form_survey(email, out):
    record = next((auth for author in authors if author['email'] == email), None)
    paper_count = int(record['papers'])

    #now we form the survey using the prepared text file
    text = ""
    for x in range(0, paper_count):
    	with open('base_survey.txt', mode='r') as f:
    		data = f.readlines()
    		text = text + data
    
    with open(out, mode='w') as g:
    	g.write(text)

for auth in authors:
	out = auth['name'].replace(' ','_') + ".txt"
	dirs = "surveys"
	form_survey(auth['email'], dirs + out)
	import_survey(out, 'application/vnd.qualtrics.survey.txt')

#Implement: dissemenation part
