# Speedtest

These scripts are part of a speedtest/netmonitor project to use a Raspberry Pi hooked up with ethernet to a router to monitor the quality of your internet. It requires

- a Raspberry Pi with a recent OS (I used Buster)
- InfluxDB installed on the Pi with authentication setup (see environment variables how to tune the scripts)
- Grafana installed to display the collected results
- These Python3 scripts setup in crontab to run regularly.


## Environment variables

You can setup the following environment variables to finetune your InfluxDB. Given that in most cases the script will run from the same host you probably only need to setup the password.

- `INFLUX_HOSTNAME` - hostname for influxdb, defaults to `localhost`
- `INFLUX_PORT` - port for the influxdb service, defaults to 8086
- `INFLUX_USERNAME` - username for influxdb, defaults to `netmonitor`
- `INFLUX_PASSWORD` - username for influxdb, defaults to ``
- `INFLUX_DATABASE` - username for influxdb, defaults to `netmonitor`
