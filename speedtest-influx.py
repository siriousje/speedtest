#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import subprocess
import datetime
import influx
import traceback

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
    influx.write_to_influxdb(payload)

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
        # starting to wonder if ping == 0 is just a faulty measurement
        if float(ping)  > 0.0:
            send_data_to_influx(time, ping, download, upload)
        else:
            print(f"ping was 0, upload: {upload}, download: {download}")

# does a single run, use speedtest-cli --list to find servers
def main():
    try:
        parse_response(subprocess.Popen('/usr/local/bin/speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8'))
    except:
        traceback.print_exc() 
        print("Unable to parse response, maybe next time")
        pass

if __name__ == '__main__':
    main()
