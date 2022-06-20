#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:chrome_devtools.py
@time:2022/06/15
"""

import PyChromeDevTools
import time
import os

os.chdir(r"C:\Program Files\Google\Chrome\Application")
cmd = "chrome.exe --remote-debugging-port=9222"
os.popen(cmd)
chrome = PyChromeDevTools.ChromeInterface()
chrome.Network.enable()
chrome.Page.enable()
chrome.Page.reload(ignoreCache=True)  # 不带缓存
start_time = time.time()
chrome.Page.navigate(url="https://www.baidu.com")
chrome.Runtime.evaluate(expression='document.getElementById("kw").value="selenium"')
chrome.wait_event("Page.loadEventFired", timeout=60)
end_time = time.time()

print("Page Loading Time:", end_time - start_time)
chrome.close()

if __name__ == '__main__':
    pass
