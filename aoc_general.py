import logging
import requests
import yaml
import sys

# Import config
with open('./config/config.yml', 'r') as ymlconfig:
    theconfig = yaml.load(ymlconfig)

# Setup log stream for stdout
log = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(sys.__stdout__)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)

# post to slack
def post(slackurl, slackmsg):
    url = slackurl
    payload={"text": slackmsg}
    r = requests.post(url, json=payload)
    return r

def postforsnow(slackurl, slackmsg, slackcolour, inc, ci):
    url = slackurl
    payload = {}
    payload['text'] = slackmsg
    attachment = payload['attachments'] = []
    payload['attachments'].append({
        'fallback ': "https://" + theconfig['snowinstance'] + ".service-now.com/nav_to.do?uri=incident.do?sys_id=" + inc['sys_id'],
        'color': slackcolour,
        'title_link': "https://" + theconfig['snowinstance'] + ".service-now.com/nav_to.do?uri=incident.do?sys_id=" + inc['sys_id'],
        'title': inc['number'],
        'thumb_url': "https://ukspafshared.blob.core.windows.net/public/servicenow.png",
        'text': "Service Plan: " + ci['u_service_plan'] + "\nIncident Priority: " + inc['priority']
    })
    r = requests.post(url, json=payload)
    return r




# condition evaluator
def evaluatecondition(itemvalue, evaluator):
    if evaluator == "greater_than":
        if itemvalue is None: # added check to see if None coming through to prevent crashes for type
            itemvalue = 0.0
            if itemvalue > theconfig['esthreshold']:
                result = True
            else:
                result = False
        else:
            if itemvalue > theconfig['esthreshold']:
                result = True
            else:
                result = False
    elif evaluator == "less_than":
        if itemvalue is None:
            itemvalue = 100.0
            if itemvalue < theconfig['esthreshold']:
                result = True
            else:
                result = False
        else:
            if itemvalue < theconfig['esthreshold']:
                result = True
            else:
                result = False
    return result