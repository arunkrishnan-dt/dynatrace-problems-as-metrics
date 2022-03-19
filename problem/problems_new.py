
def get_new_problems_payloads(problems_from_api, problems_from_file):
    # global_new_problems_by_severity = get_severity_dict_template()
    local_problem_ids = []
    for problem in problems_from_file:        
        local_problem_ids.append(problem['displayId'])        
    
    global_new_problem_count = 0
    mz_problem_count_dict = {}
    new_problem_payloads = []
    for problem in problems_from_api:
        if problem['status'] == "OPEN" and not problem['displayId'] in local_problem_ids:
            global_new_problem_count += 1             
            for management_zone in problem['managementZones']:
                mz_name = management_zone['name']
                if not mz_name in mz_problem_count_dict:
                    new_dict = {mz_name : 1}
                    mz_problem_count_dict.update(new_dict)
                else:
                    mz_problem_count_dict[mz_name] = mz_problem_count_dict[mz_name] + 1

    payload_global = "dtapi.problem.open.new.global "+ str(global_new_problem_count)
    new_problem_payloads.append(payload_global)

    for mz_name in mz_problem_count_dict:
        payload_mz = "dtapi.problem.open.new.managementZone,dt.management_zone=\""+mz_name+"\" "+ str(mz_problem_count_dict[mz_name])
        new_problem_payloads.append(payload_mz)

    return new_problem_payloads

            
    
    
