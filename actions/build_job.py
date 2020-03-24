from lib import action
import json


class BuildProject(action.JenkinsBaseAction):
    def run(self, project, parameters=None, config_override=None):
        if config_override is not None:
            self.config_override(config_override)
        if parameters is not None:
            params_list = self.parse_data(parameters)
            # Initiate job for each failing series (Server Name + Service Name)
            for params in params_list:
                job_params = { unicode(k):unicode(v) for k,v in params.items() }
                print(job_params)
                queue_num = self.jenkins.build_job(name=project, parameters=job_params, token='11b2fb5a621406e557853c8b4d116e7bfa')
                print('Remediation job {NUM} was queued for {SERVICE}'.format(NUM=queue_num, SERVICE=params['Service_Name']))
            return (True, "Success")
        else: 
            return (False, "Alert data was not provided.")

    # Parsing of Alert JSON to extract Server_Name, Service_Name, and Datacenter
    def parse_data(self, paramJson):
        params_list = []
        alertData = self.sanitize_data(paramJson)
        failing_series = alertData['failingSeries']
        for series in failing_series:
            job_params = {
                'Server_Name': series[0], 
                'Action_Type': 'Start'
            }
            
            for pointTag in series[2]:
                if "service_name=" in pointTag:
                    job_params['Service_Name'] = pointTag.split("=")[1]
                elif "datacenter=" in pointTag:
                    job_params['Datacenter'] = pointTag.split("=")[1]
            
            params_list.append(job_params)

        return params_list

    
    def sanitize_data(self, paramJson):
        print('*****ORIGINAL*****')
        print(paramJson)
        print('*****ORIGINAL*****')
        
        alertData = {}
        if isinstance(paramJson, str):
            paramJson = paramJson.replace("u'", "'").replace("'", "\"")
            print('*****MODIFIED*****')
            print(paramJson)
            print('*****MODIFIED*****')
            alertData = json.loads(paramJson)
        elif isinstance(paramJson, dict):
            alertData = paramJson
        
        return alertData
