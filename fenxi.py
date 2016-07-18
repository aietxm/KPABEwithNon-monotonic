__author__ = 'cirnotxm'

import json

with open("/Users/cirnotxm/Others/phonecrawl/1-0.txt", "rb") as f:
    j = f.read()
re = eval(j)
param ={}
for key,va in re.items():
    key.decode("utf-8")
    va.decode("utf-8")


