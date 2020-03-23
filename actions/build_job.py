from lib import action
import json


class BuildProject(action.JenkinsBaseAction):
    def run(self, project, parameters=None, config_override=None):
        if config_override is not None:
            self.config_override(config_override)
        name = parameters['alert']
        print('Alert is ' + name)
        return 1
        # return self.jenkins.build_job(project, parameters)
