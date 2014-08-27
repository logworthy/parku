import urllib2
import socket
import os
import csv
from datetime import datetime as dt
from datetime import timedelta as td
import time

socket.setdefaulttimeout(10)

token = "your_api_token_goes_here"
endpoint = "http://data.melbourne.vic.gov.au/resource/8nfq-mtcn"
extension = ".csv"
headers = [('X-App-Token', token)]
log_file = 'log.txt' # store log output here
csv_file = 'test.csv' # final data goes here
offset_file = 'offset.txt' # this keeps track of what record you're up to
sentinel_file = 'continue.txt' # delete this file to stop scraping

# number of requests you're allowed to make per hour.  city of melbourne socrata caps at 1k
request_limit = 900

# number of rows to pull per request.  i tried larger numbers but they didn't appear to work
row_limit = 1000

columns = [
'areaname',
'streetname',
'betweenstreet1',
'betweenstreet2',
'sideofstreet',
'streetmarker',
'arrivaltime',
'departuretime',
'durationseconds',
'sign',
'inviolation',
'streetid',
'deviceid'
]

opener = urllib2.build_opener()
opener.addheaders = headers

def log_function(text):
    timestamp = str(dt.now())[:-7]
    log_msg = timestamp+' - '+text
    print(log_msg)
    with open(log_file, 'a') as f:
        f.write(log_msg+'\n')

log_function('Script loaded')

requests = []

def check_requests():

    # filter to requests within the last hour
    # if the length of that list is less than the limit we're good
    return len(filter(lambda x: x > dt.now() + td(hours=-1), requests)) < request_limit
        
### loop begins

# read file and check what the last id number is
# use this to determine offset
 
def pull_data(header):

    log_function('Commencing data pull attempt')
    if not check_requests():
        # wait 4 minutes
        time.sleep(240)
        raise Exception('Made too many requests recently')

    # on start/stop we check the csv file is up to date
    # however in most cases we just use the latest offset
    if os.path.isfile(offset_file):
        with open(offset_file, 'r') as of:
            offset = int(of.read())

    else:       
        log_function('Scanning entire file for offset')
        with open(csv_file, 'r') as cf:
            cf.next()
            # log_function('First: %s' % first)
            dr = csv.DictReader(cf, fieldnames=header.split(','))
            try:
                while True:
                    last = dr.next()
            except StopIteration:
                    offset = int(last[':id'])

    log_function('Offset identified: %d' % offset)

    log_function('Sending request')

    csv_resp = opener.open(endpoint+extension+'?$select=:id,%s&$limit=%d&$offset=%d&$order=:id' % (
        ','.join(columns), row_limit, offset
        )
    )
    requests.append(dt.now())
    assert(csv_resp.getcode()==200)

    log_function('Response received, reading & writing')

    # skip first line (header)
    # BETTER: check that it matches
    read_header = csv_resp.next()
    # log_function('Header: %s' % header)
    assert(read_header == header)

    # open csv file to append to
    with open(csv_file, 'a') as cf:

        # read and write on the fly, like a pro
        for line in csv_resp:
            offset=int(line.split(',')[0])
            cf.write(line)

    with open(offset_file, 'w') as of:    
        of.write(str(offset))

    log_function('Response written')

# read the header to kick things off
with open(csv_file, 'r') as cf:
    header = cf.next()

# just rename this file to end the process
while os.path.isfile(sentinel_file):

    # attempt the extract
    try:
        pull_data(header)

    # on any errors, just wait a minute
    except Exception as e:
        log_function('Encountered error: '+str(e))
        # raise e
        time.sleep(60)

# delete the offset file on a stop so that the kick-off will always read whole thing
os.remove(offset_file)
