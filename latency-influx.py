
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import datetime
import time
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
        s.connect(('www.google.com', 80))
        s.close()
        return float((datetime.datetime.now() - start).microseconds) / 1000
    except:
        return float(30.0) # timeout

# does a single run
def single_test():
    timestamp = datetime.datetime.utcnow()
    send_data_to_influx(timestamp, time_remote_host())

# main
def main():
    # because we run once per minute and we want more data, we simply run 5 times with 10 seconds interval, should cover the timeout
    for i in range(2):
        single_test()
        time.sleep(10)

if __name__ == '__main__':
    main()