#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:jenkins_tools.py
@time:2022/06/21
"""

import jenkins
from src.utils.config_manager import get_config


class JenkinsTools:
    def __init__(self):
        self.client = jenkins.Jenkins(
            url=get_config().get('jenkins', 'url'),
            username=get_config().get('jenkins', 'username'),
            password=get_config().get('jenkins', 'api_token'))

    def get_job_last_build_url(self, job_name):
        info = self.client.get_job_info(job_name)
        last_build = info['lastCompletedBuild'] if info['lastCompletedBuild'] != info['lastBuild'] else info['lastBuild']
        return last_build['url']


if __name__ == '__main__':
    url = JenkinsTools().get_job_last_build_url("TestGroup/rpa_platform_interface_auto_test")
    print(url)
    pass
