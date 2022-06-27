#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:jmeter_script_executor.py
@time:2022/06/27
"""
import glob
import os
from src.utils.config_manager import get_root_path
import subprocess as sp
import urllib.parse


class JmeterScriptExecutor:
    def __init__(self):
        pass

    def jmeter_executor(self, script_name, num_threads, duration, hostIps='127.0.0.1'):
        """
        :param script_name: 脚本名字
        :param num_threads: 线程数
        :param duration: 执行时间
        :param hostIps: 负载参数
        :return: 启动JMeter成功
        """
        # 执行脚本名字
        runJmeterFile = '%s_%s_%s' % (script_name, num_threads, duration)
        print("执行名字脚本：%s" % runJmeterFile)
        root_dir = get_root_path()
        newdir = glob.glob(root_dir + "tests/jmeter_scripts" + os.sep + script_name + ".jmx")[0]
        # 原始脚本
        # newdir = os.path.join(thisdir, "jmeter_scripts", script_name + ".jmx")
        print("当前脚本路径: %s" % newdir)
        if not os.path.exists(newdir):
            print('脚本不存在！请检查脚本')
            return False

        # 保存测试结果路径
        resultFile = os.path.join(root_dir, 'report/jmeter', runJmeterFile)
        print("脚本执行路径: ", resultFile)

        # 判断结果路径是否存在
        if not os.path.exists(resultFile):
            os.makedirs(resultFile)

        lines = open(newdir, encoding="utf-8").readlines()
        fp = open(os.path.join(root_dir, "report/jmeter", resultFile, runJmeterFile) + '.jmx', 'w')  # 打开你要写得文件
        for s in lines:
            fp.write(s)  # 勾选通过时间判断结束
        fp.close()
        os.chdir(resultFile)
        print("当前路径: ", os.getcwd())

        # 检查环境变量
        # if self.is_evn():
        url_parse = urllib.parse.urlparse(os.environ['base_url'])
        server_host = url_parse.hostname
        server_port = url_parse.port
        # 判断分布式执行方式
        if len(hostIps.split(",")) > 2:
            # 根据自己需求添加执行类型
            Rcmd = 'jmeter -n -t %s.jmx -R %s -l %s.jtl -j %s.log' % (
                runJmeterFile, hostIps, runJmeterFile, runJmeterFile)

            # Rcmd = 'jmeter -n -t %s.jmx -R %s -l %s.jtl -j %s.log -e -o %s' % (runJmeterFile, hostIps, runJmeterFile, runJmeterFile, runJmeterFile)
            print('执行命令：%s' % Rcmd)
            # os.system(Rcmd)
        else:
            # 不生成html报告
            # cmd = 'jmeter -n -t %s.jmx -l %s.jtl -j %s.log' % (runJmeterFile, runJmeterFile, runJmeterFile, runJmeterFile)
            # 自动生成html报表
            # cmd = 'jmeter  -n -t %s.jmx -l %s.jtl -j %s.log -e -o %s' % (runJmeterFile, runJmeterFile, runJmeterFile, runJmeterFile)
            cmd = 'jmeter  -n -t %s.jmx -l %s.jtl -j %s.log -JserverHost=%s -JserverPort=%s -JthreadNum=%s -Jtime=%s -e -o %s' \
                  % (runJmeterFile, runJmeterFile, runJmeterFile, server_host, server_port, num_threads, duration, runJmeterFile)
            print('执行命令：%s' % cmd.encode('utf-8'))
            # os.system(cmd)
            p1 = sp.Popen(cmd, shell=True, stdout=sp.PIPE)
            print(p1.stdout.read())
        return resultFile + os.sep + runJmeterFile + '.jtl'

    def is_evn(self):
        """
        检查环境变量
        :return: True/False
        """
        cmd = 'jmeter -v'
        lin = os.popen(cmd)
        for i in lin:
            if 'The Apache Software Foundation' in i:
                print("Jmeter环境变量配置成功")
                return True
        else:
            print("Jmeter环境变量配置失败")
            return False


if __name__ == '__main__':
    print(get_root_path())
    os.environ['base_url'] = "http://172.19.192.44:30000"
    e = JmeterScriptExecutor().jmeter_executor("login", 1, 2)
    print("***")
    print(e)
    print("***")
    pass
