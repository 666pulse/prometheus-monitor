# Gas Monitor

## Prometheus

### config

```yml
# my global config
global:
  scrape_interval:     20s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 20s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      # - alertmanager:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'gas'

    static_configs:
    - targets: ['localhost:8000']
```

### run

```shell
prometheus --storage.tsdb.retention.time=1y --web.listen-address 0.0.0.0:9090 # prometheus service

python3 ./main.py # custom Prometheus integration
```

## Grafana

### install

```
wget https://dl.grafana.com/oss/release/grafana_9.0.0_amd64.deb

sudo dpkg -i grafana_9.0.0_amd64.deb
```

### security

```ini
; /etc/grafana/grafana.ini
# default admin user, created on startup
admin_user = admin

# default admin password, can be changed before first start of grafana,  or in profile settings
admin_password = admin
```

### change port

```ini
; /etc/grafana/grafana.ini
[server]
http_port=xxxx
```

### Start the server

```shell
sudo service grafana-server start

sudo service grafana-server status
```

## Many blockchain framework support prometheus metrics

### Tendermint

https://docs.tendermint.com/master/nodes/metrics.html

### ETH

https://dev.to/odyslam/how-to-monitor-ethereum-node-in-under-5m-3n

https://ethereum.org/en/developers/tutorials/monitoring-geth-with-influxdb-and-grafana/

### influx

https://www.influxdata.com/blog/create-bitcoin-buy-sell-alerts-influxdb/

---

Refer:

https://medium.com/@onukwilip/integrating-prometheus-into-node-express-js-app-using-the-prom-client-library-to-monitor-app-604641049556

https://opensource.com/article/19/4/weather-python-prometheus

https://grafana.com/grafana/download?edition=oss

https://grafana.com/docs/grafana/latest/installation/

https://grafana.com/docs/grafana/latest/administration/configuration/#comments-in-ini-files

<!-- https://api.weather.gov/gridpoints/RAH/73,57/forecast/hourly -->
