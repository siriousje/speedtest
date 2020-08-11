#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import subprocess
import datetime
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
def send_data_to_influx(timestamp, ping, download, upload):
    payload = [{
        "measurement" : "internet_speed",
        "time": timestamp,
        "fields" : {
            "download": float(download),
            "upload": float(upload),
            "ping": float(ping)
        }
    }]
    # host, port, user, password, database
    influx = InfluxDBClient(influx_account['hostname'], influx_account['port'], influx_account['username'], influx_account['password'], influx_account['database'])
    influx.write_points(payload)

# parses the response
def parse_response(response):
    ping = re.findall('Ping:\\s(.*?)\\s', response, re.MULTILINE)
    download = re.findall('Download:\\s(.*?)\\s', response, re.MULTILINE)
    upload = re.findall('Upload:\\s(.*?)\\s', response, re.MULTILINE)

    if len(ping) > 0 and len(download) > 0 and len(upload) > 0:
        ping = ping[0].replace(',', '.')
        download = download[0].replace(',', '.')
        upload = upload[0].replace(',', '.')
        time = datetime.datetime.utcnow()
        send_data_to_influx(time, ping, download, upload)

# does a single run
def main():
    try:
        parse_response(subprocess.Popen('/usr/local/bin/speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8'))
    except:
        print("Unable to parse response, maybe next time")
        pass

if __name__ == '__main__':
    main()
