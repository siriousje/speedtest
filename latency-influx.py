
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import datetime
import time
import os
from influxdb import InfluxDBClient

influx_account = {
    'hostname': os.getenv('INFLUX_HOSTNAME', 'localhost'),
    'port': os.getenv('INFLUX_PORT', 8086),
    'username': os.getenv('INFLUX_USERNAME', 'netmonitor'),
    'password': os.getenv('INFLUX_PASSWORD', ''),
    'database': os.getenv('INFLUX_DATABASE', 'netmonitor')
}

# sends collected data to influx
def send_data_to_influx(timestamp, latency):
    payload = [{
        "measurement" : "internet_latency",
        "time": timestamp,
        "fields" : {
            "latency": float(latency)
        }
    }]
    # host, port, user, password, database
    influx = InfluxDBClient(influx_account['hostname'], influx_account['port'], influx_account['username'], influx_account['password'], influx_account['database'])
    influx.write_points(payload)


# connects to www.google.com 
def time_remote_host():
    start = datetime.datetime.now()
    try:
        host = socket.gethostbyname("www.google.com")
        s = socket.create_connection((host, 80), 30)
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