#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import re
import subprocess
import os
import influx
import time

# sends collected data to influx
def send_data_to_influx(timestamp, public_ip):
    payload = [{
        "measurement" : "ip_history",
        "tags": {
            "public_ip": public_ip
        },
        "time": timestamp,
        "fields" : {
            "in_use": 1.0
        }
    }]
    influx.write_to_influxdb(payload)

# gets the ip address
def get_ip():
    try:
        response = subprocess.Popen('curl -s ifconfig.me/ip', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        return response
    except:
        pass
    return "unknown"

# main, gets ip, if valid ip, sends it to influx
def main():
    ip = get_ip()
    if re.match(r'^\d+\.\d+\.\d+\.\d+$', ip):
        send_data_to_influx(datetime.datetime.utcnow(), ip)

if __name__ == '__main__':
    main()
