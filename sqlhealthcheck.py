import datetime
import json
import logging
import sys
import time
import elasticsearch
import elasticsearch_dsl
import pysnow
import requests
import yaml
import aoc_elasticsearch
import aoc_servicenow
import aoc_general

# Import config
with open('./config/config.yml', 'r') as ymlconfig:
    theconfig = yaml.load(ymlconfig)

# Setup timer for loop
starttime = time.time()

# Elastic, parameters should be passed in from config
eshttpauth = (theconfig['esusername'] + ':' + theconfig['espassword'])
es = elasticsearch.Elasticsearch(hosts=[theconfig['esinstance']], http_auth=eshttpauth, timeout=10, max_retries=3, retry_on_timeout=True)
s = elasticsearch_dsl.Search(using=es, index=theconfig['esindexsearch'])
#q = Q('bool', must=[Q('range', **{'@timestamp': {'gte': "now-" + theconfig['essearchwindow']}}) & ('match', clientid=theconfig['esclientid'])])
if theconfig['esclientid'] == '':
    s = s.filter('range', **{'@timestamp': {'gte': "now-" + theconfig['essearchwindow']}})
else:
    s = s.filter('range', **{'@timestamp': {'gte': "now-" + theconfig['essearchwindow']}}).filter('match', clientid=theconfig['esclientid'])
s = s[0:0]
s.aggs.bucket("hostname", "terms", field='hostname.keyword', size=10000).pipeline('average_value', 'avg', field=theconfig['esmetric'])

print ("Search result" + s)