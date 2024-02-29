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

for file in os.listdir('/mnt/SQReports'):
    if file.endswith(".json") and "quota_report_netapp_H_drives" in file:
        mydate = file.split("_quota")[0]
        myyear = mydate[:4]
        mymonth = mydate[5:7]
        myday = mydate[8:10]
        myhour = mydate[11:13]
        myminute = mydate[14:16]
        myepoch = int(time.mktime(datetime(int(myyear), int(mymonth), int(myday), int(myhour), int(myminute)).timetuple()))
        # open file an read each opbject and send it to elasticsearch
        with open('/mnt/SQReports/' + file) as f:
            data = json.load(f)
            for line in data:
                line['@timestamp'] = convertepoch(myepoch)
                resp = es.index(index="netapp", document=line)
                print(line['@timestamp'])


