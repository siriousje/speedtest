
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import datetime
import os
import influx

# sends collected data to influx
def send_data_to_influx(timestamp, latency):
    payload = [{
        "measurement" : "internet_latency",
        "time": timestamp,
        "fields" : {
            "latency": float(latency)
        }
    }]
    influx.write_to_influxdb(payload)

# connects to www.google.com 
def time_remote_host():
    start = datetime.datetime.now()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(60)
        s.connect(('www.google.com', 80))
        s.close()
        return float((datetime.datetime.now() - start).microseconds) / 1000
    except:
        return float(60.0) # timeout

# does a single run
def main():
    timestamp = datetime.datetime.utcnow()
    send_data_to_influx(timestamp, time_remote_host())

if __name__ == '__main__':
    main()