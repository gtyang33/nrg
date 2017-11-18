qf# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 20:47:43 2017

@author: Administrator
"""

from bs4 import BeautifulSoup
import requests
newhtml='http://news.sina.com.cn/china/'
res=requests.get(newhtml)
res.recoding=
print(res)
