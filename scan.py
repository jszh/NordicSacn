import os
import pandas as pd
import math
import re

def convert(x):
    return "%d.%d.%d.%d" % (x >> 24, (x >> 16) & ((1 << 8) - 1), (x >> 8) & ((1 << 8) - 1), x & ((1 << 8) - 1))

filename = 'nordic_ip_geoloc.csv'
index_from = 40001
index_to = 46666#69934

data = pd.read_csv(filename)
print(data)
total_host = []
for index in range(index_from, index_to + 1):
    ip1 = data.ix[index]['ip1']
    ip0 = data.ix[index]['ip0']
    # ip1 = 37945855
    # ip0 = 37879552
    print("index = ", index)
    ip_range = (ip1 - ip0 + 1) // 256
    host = 0
    print(ip_range)
    for i in range(ip_range):
        ip = ip0 + i * 256
        command = "nmap -sP %s/24 --host-timeout 3s" % convert(ip)
        print(command)
        result = os.popen(command).read()
        searchObj = re.search(r'(\d+) hosts? up', result)
        if searchObj:
            host += int(searchObj.group(1))
        #    print("host =", host)
        else:
            print("search failed")
            print("result=", result)
    total_host.append(host)

with open("host_%d_%d.txt" % (index_from, index_to), 'w') as f:
    for host in total_host:
        f.write("%d\n"%host)
