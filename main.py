import os
import json
import logging
from pathlib import Path
from datetime import datetime
from configparser import ConfigParser
import pkg.log
import pkg.api as api
import pkg.encode as encode
import problem.problems_open as problems_open
import problem.problems_ttr as problems_ttr
import problem.problems_new as problems_new
import problem.problems_age as problems_age


def main(): 
    # Setup logger
    logger = logging.getLogger(__name__)
    problems_from_file = read_local_problems_file()   

    # Excution start time rounded to nearest minute
    now = datetime.now()
    time_rounded_to_nearest_minute = now.replace(second=0, microsecond=0, minute=now.minute, hour=now.hour)
    time_in_milliseconds = int(time_rounded_to_nearest_minute.timestamp() * 1000)

    # Read config
    config_obj = ConfigParser()
    config_file = Path(__file__).parent / "problems.config"
    config_obj.read(config_file)
    TENANCY_URL = config_obj["TENANCY_INFO"]["TENANCY_URL"]
    API_TOKEN   = config_obj["TENANCY_INFO"]["API_TOKEN"]    

    # Encode Token
    if encode.isEncoded(API_TOKEN):
        API_TOKEN = encode.decode(API_TOKEN)
    else:
        encoded_token = encode.encode(API_TOKEN)
        config_obj["TENANCY_INFO"]["API_TOKEN"] = encoded_token
        logger.info("Encoded token")
        update_config_file(config_obj)     

    # Get latest problems
    problems_from_api = api.get_problems(TENANCY_URL, API_TOKEN)

    # Set Metric Metadata
    if config_obj["INITIALIZE"]["METRIC_METADATA"] == "true":
        metric_metadata_payload = get_metric_metadata_payload()    
        logger.debug(metric_metadata_payload)
        api.post_metric(TENANCY_URL, API_TOKEN, metric_metadata_payload)
        config_obj["INITIALIZE"]["METRIC_METADATA"] = "false"
        logger.info("POST Metric data")
        update_config_file(config_obj)
    
    # POST Sample Dashboard "Operations Centre"
    if config_obj["INITIALIZE"]["DASHBOARD"] == "true":
        dashboard_json = read_local_dashboard_json()
        logger.info(dashboard_json)
        api.post_dashboard(TENANCY_URL, API_TOKEN, dashboard_json)
        config_obj["INITIALIZE"]["DASHBOARD"] = "false"
        logger.info("POST Dashboard")
        update_config_file(config_obj)      

    # PROBLEMS OPEN
    if config_obj["METRICS"]["PROBLEMS_OPEN"] == "true":
        all_management_zone_names = api.get_management_zones(TENANCY_URL, API_TOKEN)
        problem_open_payloads = problems_open.get_open_problems_payloads(problems_from_api, all_management_zone_names)    
        problem_open_payload = get_payload_string(problem_open_payloads, time_in_milliseconds)
        logger.debug(problem_open_payload)
        api.post_metric(TENANCY_URL,API_TOKEN,problem_open_payload)

    # Problem MTTR
    if config_obj["METRICS"]["PROBLEMS_TTR"] == "true":
        problem_ttr_payloads = problems_ttr.get_problem_ttr_payloads(problems_from_api, problems_from_file)
        problem_ttr_payload = get_payload_string(problem_ttr_payloads, time_in_milliseconds)
        logger.debug(problem_ttr_payload)
        api.post_metric(TENANCY_URL,API_TOKEN,problem_ttr_payload)

    # Problems NEW
    if config_obj["METRICS"]["PROBLEMS_NEW"] == "true":
        problem_new_payloads = problems_new.get_new_problems_payloads(problems_from_api, problems_from_file) 
        problem_new_payload = get_payload_string(problem_new_payloads, time_in_milliseconds)
        logger.debug(problem_new_payload)
        api.post_metric(TENANCY_URL,API_TOKEN,problem_new_payload)

    # Problems OLDEST AGE
    if config_obj["METRICS"]["PROBLEMS_AGE"] == "true":
        open_problems_age_payloads = problems_age.get_open_problems_age_payloads(problems_from_api, all_management_zone_names)
        open_problems_age_payload = get_payload_string(open_problems_age_payloads,time_in_milliseconds)
        logger.debug(open_problems_age_payload)
        api.post_metric(TENANCY_URL, API_TOKEN, open_problems_age_payload)

    # Write Problems to File
    write_problems_to_local_file(problems_from_api)

def update_config_file(config_obj):
    config_file = Path(__file__).parent / "problems.config"
    with open(config_file, 'w') as conf:
        config_obj.write(conf)

def get_metric_metadata_payload():
    payload = ""
    problem_open_global = "#dtapi.problem.open.global gauge dt.meta.displayName=\"Problems Open - Global\", dt.meta.description=\"Problems Open - Global\", dt.meta.unit=\"Count\""
    problem_open_mz = "#dtapi.problem.open.managementZone gauge dt.meta.displayName=\"Problems Open - Managment Zone\", dt.meta.description=\"Problems Open - Management Zone\", dt.meta.unit=\"Count\""
    payload+= problem_open_global +"\n"
    payload+= problem_open_mz +"\n"

    problem_open_new_global = "#dtapi.problem.open.new.global gauge dt.meta.displayName=\"Problems New - Global\", dt.meta.description=\"Problems New - Global\", dt.meta.unit=\"Count\""
    problem_open_new_mz = "#dtapi.problem.open.new.managementZone gauge dt.meta.displayName=\"Problems New - Managment Zone\", dt.meta.description=\"Problems New - Management Zone\", dt.meta.unit=\"Count\""
    payload+= problem_open_new_global +"\n"
    payload+= problem_open_new_mz +"\n"

    problem_ttr_global = "#dtapi.problem.ttr.global gauge dt.meta.displayName=\"Problem Time To Resolution - Global\", dt.meta.description=\"Problem Time To Resolution - Global\", dt.meta.unit=\"Minute\""
    problem_ttr_mz = "#dtapi.problem.ttr.managementZone gauge dt.meta.displayName=\"Problem Time To Resolution - Management Zone\", dt.meta.description=\"Problem Time To Resolution - Management Zone\",  dt.meta.unit=\"Minute\""
    payload+= problem_ttr_global +"\n"
    payload+= problem_ttr_mz +"\n"

    problem_oldest_global = "#dtapi.problem.open.oldest.age.global gauge dt.meta.displayName=\"Problem Oldest Age - Global\", dt.meta.description=\"Problem Oldest Age - Global\", dt.meta.unit=\"Minute\""
    problem_oldest_mz = "#dtapi.problem.open.oldest.age.managementZone gauge dt.meta.displayName=\"Problem Oldest Age - Management Zone\", dt.meta.description=\"Problem Oldest Age - Management Zone\",  dt.meta.unit=\"Minute\""
    payload+= problem_oldest_global +"\n"
    payload+= problem_oldest_mz +"\n"
    return payload

def get_payload_string(payloads_array,time_in_milliseconds):
    payload = ""
    for entry in payloads_array:
        payload += entry + " " + str(time_in_milliseconds) + '\n'
    return payload

def read_local_dashboard_json():
    dashboard_file = Path(__file__).parent / Path("assets") / "dashboard_operations_centre.json"
    f = open(dashboard_file, "r")    
    dashboard_json = json.loads(f.read())
    f.close()
    return dashboard_json

def read_local_problems_file():
    local_problems_file = Path(__file__).parent / "problems.json"
    # local_problems_file = "problems.json"  
    # Create file if not present
    if not os.path.exists(local_problems_file):        
        new_file = open(local_problems_file, "w")
        new_file.close()

    # Open local problem.json and read content
    problems_from_file=[]
    f = open(local_problems_file, "r")    
    content = f.read()
    if content != "":
        problems_from_file.extend(json.loads(content))
    f.close()
    return problems_from_file

def write_problems_to_local_file(problems_from_api):
    local_problems_file = Path(__file__).parent / "problems.json"
    f = open(local_problems_file, "w")
    f.write(json.dumps(problems_from_api))
    f.close()

if __name__ == '__main__':    
    main()
