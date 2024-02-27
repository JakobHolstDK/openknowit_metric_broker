#!/usr/bin/env python 
import subprocess
import sys
import time
import json
import os
import pprint
from elasticsearch import Elasticsearch
from datetime import datetime, timezone

def convertepoch(epoch_value):
  try:
    datetime_object = datetime.utcfromtimestamp(epoch_value)
    formatted_datetime = datetime_object.strftime('%Y-%m-%dT%H:%M:%SZ')
    return formatted_datetime
  except:
    return None

# Print the formatted datetime

es = Elasticsearch([{'host': 'dashapp01fl.unicph.domain', 'port': 9200, 'scheme': "http" }])  # Adjust the host and port as needed
# std in is streaming lines of json data

# the files are in /home/rks221/testdata called date + SQreport + .json
# list all files and save them in a dict with the data in epoch format as key
# then sort the dict and send the files to elasticsearch in order
files = {}

for file in os.listdir('/home/rks221/testdata'):
    if file.endswith(".json") and "SQreport" in file:
        mydate = file.split("SQreport")[0]
        myyear = mydate[:4]
        mymonth = mydate[4:6]
        myday = mydate[6:8]
        myepoch = int(time.mktime(datetime(int(myyear), int(mymonth), int(myday)).timetuple()))
        pprint.pprint(myepoch)

        # open file an read each opbject and send it to elasticsearch
        with open('/home/rks221/testdata/' + file) as f:
            data = json.load(f)
            for line in data:
                line['@timestamp'] = convertepoch(myepoch)
                pprint.pprint(line)
                #resp = es.index(index="isilon", document=line)
                #pprint.pprint(resp)


