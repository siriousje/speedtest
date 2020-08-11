# Speedtest

These scripts are part of a speedtest/netmonitor project to use a Raspberry Pi hooked up with ethernet to a router to monitor the quality of your internet. It requires

- a Raspberry Pi with a recent OS (I used Buster)
- InfluxDB installed on the Pi with authentication setup (see environment variables how to tune the scripts)
- Grafana installed to display the collected results
- These Python3 scripts setup in crontab to run regularly.


## installation

Clone this repository under `/opt` so that it creates `/opt/speedtest`
Then make sure to install all requirements: `sudo pip3 install -r requirements.txt`\

Copy `config.yml.sample` to `config.yml` and update the values for your installation, then add the scripts to crontab using `sudo crontab -e`

it should look something like

```
*/5 * * * * python3 /opt/speedtest/speedtest-influx.py
*/1 * * * * python3 /opt/speedtest/internet-influx.py
*/1 * * * * python3 /opt/speedtest/latency-influx.py
```

Change the numbers to what you want, I run the speedtest only once per 5 minutes


## Environment variables

You can setup the following environment variables to finetune your InfluxDB. Given that in most cases the script will run from the same host you probably only need to setup the password.

- `INFLUX_HOSTNAME` - hostname for influxdb, defaults to `localhost`
- `INFLUX_PORT` - port for the influxdb service, defaults to 8086
- `INFLUX_USERNAME` - username for influxdb, defaults to `netmonitor`
- `INFLUX_PASSWORD` - username for influxdb, defaults to ``
- `INFLUX_DATABASE` - username for influxdb, defaults to `netmonitor`
