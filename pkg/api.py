import requests
import json
import logging

logger = logging.getLogger(__name__)

def get_problems(TENANCY_URL, API_TOKEN):
    url = "https://"+TENANCY_URL+"/api/v2/problems?relativeTime=-5m&pageSize=500"
    payload={}
    headers = {  
    "Authorization": "Api-Token "+API_TOKEN
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()        
    except requests.exceptions.HTTPError as err:
        logger.error(err)
        raise SystemExit(err)
    logger.info("GET PROBLEMS :"+ str(response))
    response_json = json.loads(response.text)    
    return response_json['problems']

def get_management_zones(TENANCY_URL, API_TOKEN):
    url = "https://"+TENANCY_URL+"/api/config/v1/managementZones"
    payload={}
    headers = {  
    "Authorization": "Api-Token "+API_TOKEN
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()      
    except requests.exceptions.HTTPError as err:
        logger.error(err)
        raise SystemExit(err)
    logger.info("GET MANAGMENT ZONES :"+str(response))
    response_json = json.loads(response.text)
    management_zone_names = []
    for management_zone in response_json['values']:
        management_zone_names.append(management_zone['name'])
    return management_zone_names

def post_metric(TENANCY_URL, API_TOKEN, payload):    
    url = "https://"+TENANCY_URL+"/api/v2/metrics/ingest"
    headers = {
        "Authorization": "Api-Token "+API_TOKEN,
        "Content-Type": "text/plain"
    }
    logger.debug(payload) 
    if payload !="":
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            response.raise_for_status()        
        except requests.exceptions.HTTPError as err:
            logger.error(err)
            raise SystemExit(err)
        logger.info("POST METRIC :"+ str(response))
        logger.info(response.text)

def post_dashboard(TENANCY_URL, API_TOKEN, payload):
    url = "https://"+TENANCY_URL+"/api/config/v1/dashboards"
    headers = {
        "Authorization": "Api-Token "+API_TOKEN,
        "Content-Type": "application/json"
    }
    try:
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()        
    except requests.exceptions.HTTPError as err:
        logger.error(err)
        raise SystemExit(err)
    logger.info(response.text)


    
    
