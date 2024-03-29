from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
import pprint
import json
import redis
import os

names = ["Linux: CPU utilization", "Linux: Memory utilization", "Linux: Disk space usage", "Linux: Network traffic"]

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def print_epoch_pretty(epoch_timestamp):
    # Convert epoch timestamp to datetime object
    dt_object = datetime.utcfromtimestamp(epoch_timestamp)

    # Print the datetime object in a pretty format
    print(dt_object.strftime("%Y-%m-%d %H:%M:%S"))



def convert_epoch_to_start_of_hour(epoch_timestamp):
    # Convert epoch timestamp to datetime object
    dt_object = datetime.utcfromtimestamp(epoch_timestamp)

    # Extract year, month, day, hour
    year = dt_object.year
    month = dt_object.month
    day = dt_object.day
    hour = dt_object.hour

    # Create a new datetime object for the start of the same hour
    start_of_hour = datetime(year, month, day, hour, 0, 0)

    return start_of_hour

def convert_epoch_to_start_of_day(epoch_timestamp):
    # Convert epoch timestamp to datetime object
    dt_object = datetime.utcfromtimestamp(epoch_timestamp)

    # Extract year, month, and day
    year = dt_object.year
    month = dt_object.month
    day = dt_object.day

    # Create a new datetime object for the start of the same day (00:00:00)
    start_of_day = datetime(year, month, day, 0, 0, 0)

    return start_of_day

def connect():
  url = os.getenv('ELASTICSEARCH_URL')
  username = os.getenv('ELASTICSEARCH_USERNAME')
  password = os.getenv('ELASTICSEARCH_PASSWORD')
  es = Elasticsearch(url, basic_auth=(username, password))
  if es.info():
    return es
  else:
    return None

def register_doc(doc, index, freq="dayly"):
  myrealdoc = {}
  if freq == "hourly":
    myrealdoc['@timestamp'] = datetime.utcfromtimestamp(doc['clock'])
    mystart = convert_epoch_to_start_of_hour(doc['clock'])

  if freq == "daily":
    myrealdoc['@timestamp'] = convert_epoch_to_start_of_day(doc['clock'])
    # convert timestamp to a date object
    mystart = convert_epoch_to_start_of_day(doc['clock'])

  if freq == "all":
    myrealdoc['@timestamp'] = datetime.utcfromtimestamp(doc['clock'])
    mystart = datetime.utcfromtimestamp(doc['clock'])

  myrediskey = str(mystart) + ":" + doc['host']['name'] + ":" + doc['name']
  myredisvalue = doc['value']
  if r.exists(myrediskey):
    print("Key exists")
  else:
      myrealdoc['host'] = doc['host']['name']
      myrealdoc['metric'] = doc['name'] 
      myrealdoc['value'] = doc['value']
      create_doc(index, myrealdoc)
      r.set(myrediskey, myredisvalue)



def readndjsonfile(file):
  ndjsopnfile =  open(file) 
  count = 0 
  for line in ndjsopnfile:
       count = count + 1
       data = json.loads(line)
       print_epoch_pretty(data['clock'])
       register_doc(data, "zabbix", "all")
  return True

def readjsonfile(file):
  try:
    with open(file  , 'r') as f:
      myfiledata = f.read()
  except:
    return None
  
  try:
    data = json.loads(myfiledata)
  except:
    return None

  return data

def create_doc(index, doc):
  es = connect()
  try:
    resp = es.index(index=index, body=doc)
    return resp
  except:
    return None
  
def create_index(index):
  es = connect()
  try:
    resp = es.indices.create(index=index)
    return resp
  except:
    return True



def main():
  create_index("zabbix")
  filename = "data/history.ndjson"
  readndjsonfile(filename)

if __name__ == "__main__":
  main()



