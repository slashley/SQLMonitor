import elasticsearch
import elasticsearch_dsl
import datetime
import yaml

# Import config
with open('./config/config.yml', 'r') as ymlconfig:
    theconfig = yaml.load(ymlconfig)

# function for updating CI status in elasticsearch
def update_esheartbeat(ciname, clientid, cistatus):
    eshttpauth = (theconfig['esusername'] + ':' + theconfig['espassword'])
    es = elasticsearch.Elasticsearch(hosts=[theconfig['esinstance']], http_auth=eshttpauth, timeout=5, max_retries=3, retry_on_timeout=True)
    #s = elasticsearch_dsl.Search(using=es, index=theconfig[''])
    #s = s.filter("range", **{'@timestamp': {'gte': 'now-1m'}})
    #s = s[0:0]
    cidoc = { 'name': ciname, 'Heartbeat_Status': cistatus, 'clientid': clientid, 'timestamp': datetime.datetime.now() }
    es.index(index=theconfig['esindexupdate'], doc_type='doc', body=cidoc)