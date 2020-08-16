
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import re
import subprocess
import os
import influx
import time

hosts = ['www.google.com', 'www.xs4all.nl', 'www.netflix.com', 'www.sirious.net']

# sends collected data to influx
def send_data_to_influx(timestamp, host, latency):
    payload = [{
        "measurement" : "internet_latency",
        "tags": {
            "host": host
        },
        "time": timestamp,
        "fields" : {
            "latency": float(latency)
        }
    }]
    influx.write_to_influxdb(payload)

# connects to www.google.com 
def ping_remote_host(host):
    try:
        response = subprocess.Popen('ping -c 1 www.google.com', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        ping = re.findall('time=(.*?)\\sms', response, re.MULTILINE)
        if len(ping) > 0:
            ping = ping = ping[0].replace(',', '.')
            return float(ping)
    except:
        pass
    return float(-1.0)

# does a single run
def single_test():
    for host in hosts:
        send_data_to_influx(datetime.datetime.utcnow(), host, ping_remote_host(host))

# does multiple
def main():
    for i in range(5): # again 5 should be ok as the tests also take a bit of time
        single_test()
        time.sleep(10)

if __name__ == '__main__':
    main()