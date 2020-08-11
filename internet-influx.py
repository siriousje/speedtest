
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import datetime
import time
import influx

# sends collected data to influx
def send_data_to_influx(timestamp, up):
    payload = [{
        "measurement" : "internet_up",
        "time": timestamp,
        "fields" : {
            "up": float(up)
        }
    }]
    influx.write_to_influxdb(payload)

# connects to google's nameserver with a timeout of 3 seconds
def ping_remote_host():
    try:
        socket.setdefaulttimeout(3)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        return True
    except:
        return False

# does a single run
def single_test():
    timestamp = datetime.datetime.utcnow()
    if ping_remote_host():
        send_data_to_influx(timestamp, 1)
    else:
        send_data_to_influx(timestamp, 0)

# main
def main():
    # because we run once per minute and we want more data, we simply run 5 times with 10 seconds interval, should cover the timeout
    for i in range(5):
        single_test()
        time.sleep(10)

if __name__ == '__main__':
    main()