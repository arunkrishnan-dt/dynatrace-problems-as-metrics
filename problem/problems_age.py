import time

def get_minutes(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    return int(minutes)

def get_global_problem_oldest_age(problems_from_api):
    problem_ages = []
    curr_time = time.time() * 1000
    for problem in problems_from_api:
        if problem['status'] == "OPEN":
            problem_start_time = problem['startTime']
            problem_age = get_minutes(curr_time - problem_start_time)
            problem_ages.append(problem_age)
    if len(problem_ages) == 0:
        problem_ages.append(0)
    problem_ages.sort(reverse=True)    
    return int(problem_ages[0])

def get_global_problem_oldest_payload(problems_from_api):
    payloads = []
    oldest_age = get_global_problem_oldest_age(problems_from_api)
    payload = "dtapi.problem.open.oldest.age.global "+ str(oldest_age)
    payloads.append(payload)
    return payloads

def get_mz_problem_oldest_age(problems_from_api):
    curr_time = time.time() * 1000
    mz_problem_age_dict = {}
    for problem in problems_from_api:
        if problem['status'] == "OPEN":
            problem_start_time = problem['startTime']
            problem_age = get_minutes(curr_time - problem_start_time)
            for management_zone in problem['managementZones']:
                mz_name = management_zone['name']
                if not mz_name in mz_problem_age_dict:
                    new_dict = {mz_name: problem_age}
                    mz_problem_age_dict.update(new_dict)
                else:
                    if mz_problem_age_dict[mz_name] < problem_age:
                        mz_problem_age_dict[mz_name] = problem_age
    return mz_problem_age_dict

def get_mz_problem_oldest_payloads(problems_from_api):
    payloads=[]
    mz_problem_age_dict = get_mz_problem_oldest_age(problems_from_api)
    for mz_name in mz_problem_age_dict:
        payload = "dtapi.problem.open.oldest.age.managementZone,dt.management_zone=\""+mz_name+"\" "+ str(mz_problem_age_dict[mz_name])
        payloads.append(payload)
    return payloads

def get_mz_without_problems_payloads(problems_from_api, all_management_zone_names):
    mz_without_problems_payloads = []
    management_zones_with_problems = []    
    for problem in problems_from_api:
        if problem['status'] == "OPEN":
            for management_zone in problem['managementZones']:
                mz_name = management_zone['name']
                management_zones_with_problems.append(mz_name)
    
    for mz_name in all_management_zone_names:
        if not mz_name in management_zones_with_problems:
            payload = "dtapi.problem.open.oldest.age.managementZone,dt.management_zone=\""+mz_name+"\" 0"
            mz_without_problems_payloads.append(payload)
    
    return mz_without_problems_payloads

def get_open_problems_age_payloads(problems_from_api, all_management_zone_names):
    open_problems_age_payloads = []
    # Global
    global_problem_oldest_age_payload = get_global_problem_oldest_payload(problems_from_api)
    # Management Zones
    mz_problem_oldest_age_payloads = get_mz_problem_oldest_payloads(problems_from_api)
    # Management Zones without problems
    mz_without_problems_payloads = get_mz_without_problems_payloads(problems_from_api, all_management_zone_names)

    open_problems_age_payloads = open_problems_age_payloads + global_problem_oldest_age_payload + mz_problem_oldest_age_payloads + mz_without_problems_payloads

    return open_problems_age_payloads

    
    




    